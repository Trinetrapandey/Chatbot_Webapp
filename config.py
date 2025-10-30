"""
Configuration Management Module
Handles environment variables and application settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Central configuration class"""
    
    # Pinecone Configuration
    PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
    PINECONE_CLOUD = "aws"
    PINECONE_REGION = "us-east-1"
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
    AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
    AZURE_DEPLOYMENT_NAME = os.environ.get("DEPLOYMENT_NAME")
    AZURE_API_VERSION = "2024-02-01"
    AZURE_EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
    AZURE_EMBEDDING_MODEL = "text-embedding-3-small"
    AZURE_EMBEDDING_API_VERSION = "2023-05-15"
    
    # HuggingFace Configuration
    HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
    HUGGINGFACE_MODEL_REPO = "microsoft/DialoGPT-large"
    
    # Model Parameters
    DEFAULT_TEMPERATURE = 0.7
    MAX_TOKENS_AZURE = 800
    MAX_LENGTH_HUGGINGFACE = 512
    EMBEDDING_CHUNK_SIZE = 1000
    
    # Text Processing Configuration
    TEXT_CHUNK_SIZE = 1000
    TEXT_CHUNK_OVERLAP = 200
    TEXT_SEPARATORS = ["\n\n", "\n", ". ", "! ", "? ", " ", ""]
    
    # Vector Store Configuration
    VECTOR_DIMENSION = 1536
    VECTOR_METRIC = "cosine"
    RETRIEVAL_K = 3
    
    # System Prompts
    SYSTEM_PROMPTS = {
        "Helpful Assistant (Default)": "You are a helpful AI assistant. Provide clear, concise, and accurate responses.",
        "Technical Expert": "You are a technical expert. Provide detailed, accurate technical information and explanations.",
        "Creative Writer": "You are a creative writer. Respond with imaginative, engaging, and creative content.",
        "Formal Business Assistant": "You are a formal business assistant. Provide professional, concise, and business-appropriate responses.",
        "Casual Friendly Helper": "You are a casual, friendly helper. Respond in a warm, conversational tone."
    }
    
    @classmethod
    def validate_azure_config(cls):
        """Validate Azure OpenAI configuration"""
        required = [cls.AZURE_OPENAI_KEY, cls.AZURE_OPENAI_ENDPOINT, cls.AZURE_DEPLOYMENT_NAME]
        if not all(required):
            raise EnvironmentError("Azure OpenAI credentials not set in environment")
        return True
    
    @classmethod
    def validate_pinecone_config(cls):
        """Validate Pinecone configuration"""
        if not cls.PINECONE_API_KEY:
            raise EnvironmentError("PINECONE_API_KEY not set in environment")
        return True
    
    @classmethod
    def validate_huggingface_config(cls):
        """Validate HuggingFace configuration"""
        if not cls.HUGGINGFACE_API_KEY:
            raise EnvironmentError("HUGGINGFACE_API_KEY not set in environment")
        return True