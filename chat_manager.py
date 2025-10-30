"""
Chat Manager Module
Handles conversation chains and response generation
"""
from langchain.chains import RetrievalQA, LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from model_manager import ModelManager
from pdf_processor import PDFProcessor
from config import Config


class ChatManager:
    """Manages conversation chains and AI responses"""
    
    def __init__(self):
        self.model_manager = ModelManager()
        self.pdf_processor = PDFProcessor(self.model_manager)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
    def initialize_system(self):
        """Initialize the complete system"""
        return self.model_manager.initialize_components()
    
    def create_rag_chain(self, system_prompt):
        """Create RAG chain with custom system prompt"""
        if not self.pdf_processor.vectorstore:
            raise ValueError("No vector store available. Please process a PDF first.")
        
        prompt_template = """{system_prompt}

Use the following pieces of context to answer the question at the end.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}

Answer: """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["system_prompt", "context", "question"]
        )
        
        # Create the retrieval chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.model_manager.current_model,
            chain_type="stuff",
            retriever=self.pdf_processor.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": Config.RETRIEVAL_K}
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
        # Create a wrapper function to handle the system_prompt input
        def rag_wrapper(inputs):
            query = inputs.get("query", "") if isinstance(inputs, dict) else inputs
            result = qa_chain.invoke({
                "query": query,
                "system_prompt": system_prompt
            })
            return result
        
        return rag_wrapper
    
    def create_conversation_chain(self, system_prompt):
        """Create regular conversation chain with custom system prompt"""
        if self.model_manager.model_type == "azure":
            # For Azure OpenAI (Chat model)
            prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_prompt),
                HumanMessagePromptTemplate.from_template("{input}")
            ])
        else:
            # For HuggingFace (non-chat model)
            prompt = PromptTemplate(
                template=f"{system_prompt}\n\nQuestion: {{input}}\nAnswer:",
                input_variables=["input"]
            )
        
        return LLMChain(
            llm=self.model_manager.current_model,
            prompt=prompt,
            memory=self.memory,
            verbose=False
        )
    
    def get_response(self, question, system_prompt, use_rag=False):
        """
        Get response from the AI model
        Returns: (response_text, source_documents)
        """
        try:
            if not self.model_manager.is_initialized():
                return "No model initialized. Please select and initialize a model first.", []
            
            if use_rag and not self.pdf_processor.vectorstore:
                return "RAG is enabled but no PDF has been processed. Please process a PDF first or disable RAG.", []

            # RAG response
            if use_rag and self.pdf_processor.vectorstore:
                try:
                    chain = self.create_rag_chain(system_prompt)
                    result = chain({"query": question})
                    return result["result"], result.get("source_documents", [])
                except Exception as e:
                    # Fallback: try without system_prompt if there's an issue
                    try:
                        qa_chain = RetrievalQA.from_chain_type(
                            llm=self.model_manager.current_model,
                            chain_type="stuff",
                            retriever=self.pdf_processor.vectorstore.as_retriever(
                                search_kwargs={"k": Config.RETRIEVAL_K}
                            ),
                            return_source_documents=True
                        )
                        result = qa_chain.invoke({"query": question})
                        return result["result"], result.get("source_documents", [])
                    except Exception as fallback_error:
                        return f"RAG Error: {str(fallback_error)}", []
            
            # Regular conversation response
            else:
                chain = self.create_conversation_chain(system_prompt)
                
                if self.model_manager.model_type == "azure":
                    result = chain.invoke({"input": question})
                    return result["text"], []
                else:
                    # HuggingFace models
                    result = chain.invoke({"input": question})
                    return result["text"], []
                
        except Exception as e:
            return f"Error generating response: {str(e)}", []
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
    
    def reset_system(self):
        """Reset entire system"""
        self.clear_memory()
        self.pdf_processor.vectorstore = None
        self.pdf_processor.current_index_name = None
        self.model_manager.current_model = None
        self.model_manager.model_type = None