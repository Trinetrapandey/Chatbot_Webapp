"""
UI Components Module
Reusable UI components for Streamlit interface
"""
import streamlit as st
from styles import get_feature_card_html
from config import Config


def render_model_selection(chat_manager, session_state):
    """Render model selection section"""
    st.subheader("🤖 Model Selection")
    model_type = st.radio(
        "Choose AI Model:",
        ["azure", "huggingface"],
        format_func=lambda x: "Azure OpenAI" if x == "azure" else "HuggingFace",
        index=0 if session_state.model_type == "azure" else 1
    )
    
    # Initialize model button
    if not session_state.model_initialized or model_type != session_state.model_type:
        if st.button("Initialize Model", type="primary", use_container_width=True):
            with st.spinner(f"Initializing {model_type} model..."):
                try:
                    if model_type == "azure":
                        success = chat_manager.model_manager.initialize_azure_model()
                    else:
                        success = chat_manager.model_manager.initialize_huggingface_model()
                    
                    if success:
                        session_state.model_type = model_type
                        session_state.model_initialized = True
                        st.success(f"{model_type.upper()} model initialized successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to initialize {model_type} model: {str(e)}")
    
    # Show model status
    if session_state.model_initialized:
        st.success(f"✅ {session_state.model_type.upper()} model is ready!")
    else:
        st.warning("⚠️ Please initialize a model first")


def render_system_prompt_selection(session_state):
    """Render system prompt selection section"""
    st.subheader("📝 System Prompt")
    system_prompt_option = st.selectbox(
        "Choose System Prompt Style:",
        list(Config.SYSTEM_PROMPTS.keys()) + ["Custom"]
    )
    
    if system_prompt_option == "Custom":
        system_prompt = st.text_area(
            "Custom System Prompt:",
            value=session_state.system_prompt,
            height=100,
            help="Define the AI's behavior, personality, and response style"
        )
    else:
        system_prompt = Config.SYSTEM_PROMPTS[system_prompt_option]
    
    if system_prompt != session_state.system_prompt:
        session_state.system_prompt = system_prompt
        # Clear chat history when prompt changes for consistency
        session_state.messages = []
        session_state.chat_manager.clear_memory()


def render_rag_settings(chat_manager, session_state):
    """Render RAG settings section"""
    st.subheader("📚 RAG Settings")
    use_rag = st.checkbox(
        "Enable RAG (Retrieval Augmented Generation)",
        value=session_state.use_rag,
        help="Use document context for responses. Disable for general knowledge mode.",
        disabled=not session_state.model_initialized
    )
    
    if use_rag != session_state.use_rag:
        session_state.use_rag = use_rag
        st.rerun()
    
    if use_rag:
        st.info("RAG is enabled. Upload a PDF to use document context.")
        
        # Pinecone Index Name
        index_name = st.text_input(
            "Pinecone Index Name",
            value="pdf-chatbot-index",
            help="Name of the Pinecone index to use"
        )
        
        # PDF Upload for RAG
        uploaded_file = st.file_uploader(
            "Upload PDF for RAG",
            type="pdf",
            help="Document will be processed for contextual responses"
        )
        
        if uploaded_file and not session_state.processed:
            if st.button("🚀 Process PDF", use_container_width=True, type="primary"):
                process_pdf_with_status(chat_manager, uploaded_file, index_name, session_state)
        elif session_state.processed:
            st.success("✅ PDF processed and ready for RAG!")
            if chat_manager.pdf_processor.current_index_name:
                st.info(f"Using Pinecone index: {chat_manager.pdf_processor.current_index_name}")


def process_pdf_with_status(chat_manager, uploaded_file, index_name, session_state):
    """Process PDF with status updates"""
    status_container = st.empty()
    
    def status_callback(message):
        status_container.status(message, expanded=True)
    
    with st.spinner("Processing PDF..."):
        success, message = chat_manager.pdf_processor.process_pdf(
            uploaded_file, 
            index_name,
            status_callback
        )
        if success:
            session_state.processed = True
            st.success(message)
            st.rerun()
        else:
            st.error(message)


def render_chat_management(session_state):
    """Render chat management buttons"""
    st.subheader("💬 Chat Management")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Chat", use_container_width=True):
            session_state.messages = []
            session_state.chat_manager.clear_memory()
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            session_state.messages = []
            session_state.chat_manager.reset_system()
            session_state.processed = False
            session_state.model_initialized = False
            st.rerun()


def render_system_status(session_state, chat_manager):
    """Render system status section"""
    st.subheader("📊 System Status")
    st.write(f"**Model:** {session_state.model_type.upper()}")
    st.write(f"**Model Status:** {'✅ Ready' if session_state.model_initialized else '❌ Not Ready'}")
    
    if session_state.use_rag:
        rag_status = "✅ Ready" if session_state.processed else "⏳ Waiting for PDF"
        st.write(f"**RAG:** {rag_status}")
    else:
        st.write("**RAG:** ❌ Disabled")
    
    st.write(f"**Messages:** {len(session_state.messages)}")
    st.write(f"**Memory:** {'✅ Active' if session_state.chat_manager.memory else '❌ Inactive'}")
    
    if session_state.processed and chat_manager.pdf_processor.current_index_name:
        st.write(f"**Pinecone Index:** {chat_manager.pdf_processor.current_index_name}")


def render_features_panel():
    """Render features panel"""
    st.subheader("🎯 Features")
    
    features = [
        ("🔧 Custom System Prompt", "Multiple personality options or custom prompts"),
        ("🤖 Multi-Model Support", "Switch between Azure OpenAI and HuggingFace"),
        ("🌲 Pinecone Vector DB", "Cloud-based vector database for scalability"),
        ("📚 Smart RAG", "Document-aware responses with context"),
        ("💭 Conversation Memory", "Maintains context across messages")
    ]
    
    for title, description in features:
        st.markdown(get_feature_card_html(title, description), unsafe_allow_html=True)
    
    # Quick tips
    st.subheader("💡 Tips")
    st.info("""
    - **Select model type** and click Initialize
    - **Choose system prompt** style or create custom
    - **Enable RAG** and upload PDF for document context
    - **Start chatting** with your configured AI assistant
    - **Pinecone** provides cloud-based vector storage
    """)


def render_chat_metrics(session_state):
    """Render chat configuration metrics"""
    config_col1, config_col2, config_col3, config_col4 = st.columns(4)
    with config_col1:
        st.metric("Model", session_state.model_type.upper())
    with config_col2:
        rag_status = "Enabled" if session_state.use_rag else "Disabled"
        st.metric("RAG", rag_status)
    with config_col3:
        st.metric("PDF Ready", "✅" if session_state.processed else "❌")
    with config_col4:
        db_type = "Pinecone" if session_state.processed else "None"
        st.metric("Vector DB", db_type)