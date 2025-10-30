"""
PDF Processor Module
Handles PDF reading, text extraction, and chunking
"""
import os
import tempfile
import time
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
from config import Config


class PDFProcessor:
    """Handles PDF processing and vector store creation"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.vectorstore = None
        self.current_index_name = None
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            reader = PdfReader(pdf_path)
            pages = [p.extract_text() for p in reader.pages]
            # Filter out None or empty pages
            pages = [p.strip() for p in pages if p and p.strip()]
            text = "\n".join(pages)

            if not text.strip():
                raise ValueError("No text could be extracted from the PDF file.")
            
            return text, len(pages)
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def split_text_into_chunks(self, text):
        """Split text into smaller chunks"""
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=Config.TEXT_CHUNK_SIZE,
                chunk_overlap=Config.TEXT_CHUNK_OVERLAP,
                length_function=len,
                separators=Config.TEXT_SEPARATORS
            )
            texts = text_splitter.split_text(text)
            
            if not texts:
                raise ValueError("No text chunks were created from the PDF.")
            
            return texts
        except Exception as e:
            raise Exception(f"Error splitting text: {str(e)}")
    
    def test_embeddings(self, sample_text):
        """Test embedding generation"""
        try:
            vector = self.model_manager.embeddings.embed_query(sample_text)
            return len(vector)
        except Exception as e:
            raise Exception(f"Embedding test failed: {str(e)}")
    
    def setup_pinecone_index(self, index_name):
        """Create or connect to Pinecone index"""
        try:
            existing_indexes = self.model_manager.pc.list_indexes().names()
            
            if index_name not in existing_indexes:
                # Create new index
                self.model_manager.pc.create_index(
                    name=index_name,
                    dimension=Config.VECTOR_DIMENSION,
                    metric=Config.VECTOR_METRIC,
                    spec=ServerlessSpec(
                        cloud=Config.PINECONE_CLOUD,
                        region=Config.PINECONE_REGION
                    )
                )
                
                # Wait for index to be ready
                for i in range(30):  # Wait up to 30 seconds
                    index_info = self.model_manager.pc.describe_index(index_name)
                    if index_info.status['ready']:
                        break
                    time.sleep(1)
                else:
                    raise Exception("Pinecone index creation timeout")
                
                return True, "created"
            else:
                return True, "existing"
                
        except Exception as e:
            raise Exception(f"Error setting up Pinecone index: {str(e)}")
    
    def create_documents(self, text_chunks):
        """Create Document objects from text chunks"""
        return [Document(page_content=text) for text in text_chunks]
    
    def upload_to_pinecone(self, documents, index_name):
        """Upload documents to Pinecone vector store"""
        try:
            self.vectorstore = PineconeVectorStore.from_documents(
                documents=documents,
                embedding=self.model_manager.embeddings,
                index_name=index_name
            )
            self.current_index_name = index_name
            return True
        except Exception as e:
            raise Exception(f"Failed to upload to Pinecone: {str(e)}")
    
    def process_pdf(self, uploaded_file, index_name="pdf-chatbot-index", status_callback=None):
        """
        Process uploaded PDF and create vector store using Pinecone
        status_callback: optional function to report progress
        """
        # Save uploaded file to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name

        try:
            # Step 1: Read PDF
            if status_callback:
                status_callback("Reading PDF document...")
            text, num_pages = self.extract_text_from_pdf(pdf_path)
            if status_callback:
                status_callback(f"PDF Read Successfully - {num_pages} pages")

            # Step 2: Split text into chunks
            if status_callback:
                status_callback("Splitting text into chunks...")
            texts = self.split_text_into_chunks(text)
            if status_callback:
                status_callback(f"Created {len(texts)} text chunks")

            # Step 3: Test embedding
            if status_callback:
                status_callback("Testing embeddings...")
            vector_dim = self.test_embeddings(texts[0])
            if status_callback:
                status_callback(f"Vector Dimension: {vector_dim}")

            # Step 4: Setup Pinecone index
            if status_callback:
                status_callback("Setting up Pinecone index...")
            success, index_status = self.setup_pinecone_index(index_name)
            if status_callback:
                status_msg = f"{'Created new' if index_status == 'created' else 'Using existing'} Pinecone index: {index_name}"
                status_callback(status_msg)

            # Step 5: Create documents
            if status_callback:
                status_callback("Creating document vectors...")
            documents = self.create_documents(texts)
            if status_callback:
                status_callback(f"Prepared {len(documents)} documents")

            # Step 6: Upload to Pinecone
            if status_callback:
                status_callback("Uploading to Pinecone...")
            self.upload_to_pinecone(documents, index_name)
            if status_callback:
                status_callback("Vector Store Ready in Pinecone!")
           
            return True, f"PDF processed successfully! Created {len(documents)} chunks from {num_pages} pages."
        
        except Exception as e:
            return False, f"Error processing PDF: {str(e)}"
        finally:
            # Clean up temporary file
            if os.path.exists(pdf_path):
                try:
                    os.unlink(pdf_path)
                except:
                    pass