# Advanced RAG Chatbot - Modularized Structure

## 📁 Project Structure

```
rag-chatbot/
├── app.py                    # Main application entry point
├── config.py                 # Configuration and environment variables
├── model_manager.py          # AI model initialization and management
├── pdf_processor.py          # PDF processing and vector store creation
├── chat_manager.py           # Conversation chains and response generation
├── ui_components.py          # Reusable Streamlit UI components
├── styles.py                 # CSS styling and HTML templates
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in repo)
└── README.md                 # Project documentation
```

## 📋 Module Descriptions

### 1. **config.py**
Central configuration management for the entire application.

**Responsibilities:**
- Environment variable loading
- Application constants and settings
- Configuration validation
- System prompts definitions

**Key Classes:**
- `Config`: Central configuration class with validation methods

### 2. **styles.py**
UI styling and HTML template generation.

**Responsibilities:**
- Custom CSS definitions
- HTML template functions
- Consistent styling across the app

**Key Functions:**
- `get_header_html()`: Main header template
- `get_feature_card_html()`: Feature card template
- `get_chat_message_html()`: Chat message formatting

### 3. **model_manager.py**
Manages AI model initialization and embeddings.

**Responsibilities:**
- Azure OpenAI model initialization
- HuggingFace model initialization
- Embedding model setup
- Pinecone client initialization

**Key Classes:**
- `ModelManager`: Handles all model-related operations

### 4. **pdf_processor.py**
Handles PDF processing and vector store operations.

**Responsibilities:**
- PDF text extraction
- Text chunking and splitting
- Pinecone index management
- Document vectorization and upload

**Key Classes:**
- `PDFProcessor`: Complete PDF processing pipeline

### 5. **chat_manager.py**
Manages conversation chains and response generation.

**Responsibilities:**
- RAG chain creation
- Conversation chain creation
- Response generation
- Memory management

**Key Classes:**
- `ChatManager`: Orchestrates chat functionality

### 6. **ui_components.py**
Reusable Streamlit UI components.

**Responsibilities:**
- Model selection UI
- System prompt configuration
- RAG settings interface
- Chat management controls
- Status displays

**Key Functions:**
- `render_model_selection()`: Model selection interface
- `render_system_prompt_selection()`: Prompt configuration
- `render_rag_settings()`: RAG configuration
- `render_chat_management()`: Chat controls
- `render_system_status()`: System status display

### 7. **app.py**
Main application entry point and orchestration.

**Responsibilities:**
- Streamlit page configuration
- Session state initialization
- Component orchestration
- Main application flow

**Key Functions:**
- `main()`: Application entry point
- `initialize_session_state()`: Session initialization
- `render_sidebar()`: Sidebar rendering
- `render_chat_interface()`: Chat interface rendering

## 🚀 Setup Instructions

### 1. Create Project Directory
```bash
mkdir rag-chatbot
cd rag-chatbot
```

### 2. Create All Module Files
Create each file from the artifacts above in the project directory.

### 3. Create .env File
```env
# Azure OpenAI Configuration
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
DEPLOYMENT_NAME=your_deployment_name

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key

# HuggingFace Configuration (Optional)
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Application
```bash
streamlit run app.py
```

## 🔄 Data Flow

```
User Input
    ↓
app.py (Main Entry)
    ↓
chat_manager.py (Process Request)
    ↓
    ├─→ model_manager.py (AI Model)
    │       ↓
    │   Response Generation
    │
    └─→ pdf_processor.py (RAG Mode)
            ↓
        Vector Store Retrieval
            ↓
        Context-Enhanced Response
```

## 🎯 Key Features by Module

### Configuration Management (config.py)
- ✅ Centralized configuration
- ✅ Environment validation
- ✅ Easy parameter adjustments

### Model Management (model_manager.py)
- ✅ Multiple model support (Azure, HuggingFace)
- ✅ Embedding initialization
- ✅ Pinecone integration

### PDF Processing (pdf_processor.py)
- ✅ PDF text extraction
- ✅ Smart text chunking
- ✅ Vector store creation
- ✅ Pinecone index management

### Chat Management (chat_manager.py)
- ✅ RAG chain creation
- ✅ Conversation memory
- ✅ System prompt integration
- ✅ Response generation

### UI Components (ui_components.py)
- ✅ Modular UI elements
- ✅ Reusable components
- ✅ Consistent styling
- ✅ Status displays

## 🛠️ Customization Guide

### Adding a New AI Model
1. Add configuration in `config.py`
2. Create initialization method in `model_manager.py`
3. Update UI in `ui_components.py`

### Changing Vector Store
1. Update configuration in `config.py`
2. Modify `pdf_processor.py` to use new vector store
3. Adjust retrieval settings

### Adding New System Prompts
1. Add to `Config.SYSTEM_PROMPTS` in `config.py`
2. UI will automatically update

### Customizing UI
1. Modify CSS in `styles.py`
2. Update component functions in `ui_components.py`
3. Adjust layout in `app.py`

## 📊 Benefits of Modularization

1. **Maintainability**: Each module has a single responsibility
2. **Testability**: Modules can be tested independently
3. **Reusability**: Components can be reused across projects
4. **Scalability**: Easy to add new features
5. **Readability**: Clear separation of concerns
6. **Debugging**: Easier to locate and fix issues

## 🔍 Troubleshooting

### Import Errors
- Ensure all modules are in the same directory
- Check that `requirements.txt` is installed

### Configuration Errors
- Verify `.env` file exists and has correct values
- Check `config.py` validation methods

### Model Initialization Failures
- Verify API keys are correct
- Check network connectivity
- Review error messages in `model_manager.py`

## 📝 Notes

- All modules are designed to work together seamlessly
- Session state is managed in `app.py` and passed to components
- Error handling is implemented at each layer
- The modular structure allows for easy extension and maintenance