"""
Model Manager Module
Handles initialization and management of AI models and embeddings
"""
from pinecone import Pinecone
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.llms import HuggingFaceEndpoint
from config import Config


class ModelManager:
    """Manages AI models and embeddings"""
    
    def __init__(self):
        self.current_model = None
        self.model_type = None
        self.embeddings = None
        self.pc = None
        
    def initialize_components(self):
        """Initialize embeddings and Pinecone"""
        try:
            # Validate configuration
            Config.validate_pinecone_config()
            Config.validate_azure_config()

            # Initialize Pinecone
            self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)

            # Initialize embeddings
            self.embeddings = AzureOpenAIEmbeddings(
                azure_deployment=Config.AZURE_EMBEDDING_DEPLOYMENT,
                model=Config.AZURE_EMBEDDING_MODEL,
                openai_api_type="azure",
                openai_api_key=Config.AZURE_OPENAI_KEY,
                azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
                openai_api_version=Config.AZURE_EMBEDDING_API_VERSION,
                chunk_size=Config.EMBEDDING_CHUNK_SIZE
            )
            
            return True
            
        except Exception as e:
            raise Exception(f"Error initializing components: {str(e)}")
    
    def initialize_azure_model(self):
        """Initialize Azure OpenAI model"""
        try:
            Config.validate_azure_config()
            
            model = AzureChatOpenAI(
                azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
                api_key=Config.AZURE_OPENAI_KEY,
                api_version=Config.AZURE_API_VERSION,
                deployment_name=Config.AZURE_DEPLOYMENT_NAME,
                temperature=Config.DEFAULT_TEMPERATURE,
                max_tokens=Config.MAX_TOKENS_AZURE
            )
            self.current_model = model
            self.model_type = "azure"
            return True
            
        except Exception as e:
            raise Exception(f"Error initializing Azure model: {str(e)}")
    
    def initialize_huggingface_model(self):
        """Initialize HuggingFace model"""
        try:
            Config.validate_huggingface_config()
            
            model = HuggingFaceEndpoint(
                repo_id=Config.HUGGINGFACE_MODEL_REPO,
                huggingfacehub_api_token=Config.HUGGINGFACE_API_KEY,
                temperature=Config.DEFAULT_TEMPERATURE,
                max_length=Config.MAX_LENGTH_HUGGINGFACE
            )
            self.current_model = model
            self.model_type = "huggingface"
            return True
            
        except Exception as e:
            raise Exception(f"Error initializing HuggingFace model: {str(e)}")
    
    def get_current_model_info(self):
        """Get current model information"""
        if self.model_type == "azure":
            return "Azure OpenAI"
        elif self.model_type == "huggingface":
            return "HuggingFace"
        else:
            return "No model selected"
    
    def is_initialized(self):
        """Check if model is initialized"""
        return self.current_model is not None