"""
Main Application Module
Entry point for the Streamlit RAG Chatbot application
"""
import streamlit as st
from chat_manager import ChatManager
from styles import CUSTOM_CSS, get_header_html, get_chat_message_html
from ui_components import (
    render_model_selection,
    render_system_prompt_selection,
    render_rag_settings,
    render_chat_management,
    render_system_status,
    render_features_panel,
    render_chat_metrics
)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'chat_manager' not in st.session_state:
        st.session_state.chat_manager = ChatManager()
        # Initialize system components
        try:
            if not st.session_state.chat_manager.initialize_system():
                st.error("Failed to initialize system components. Please check your environment variables.")
        except Exception as e:
            st.error(f"Error initializing system: {str(e)}")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = "You are a helpful AI assistant. Provide clear, concise, and accurate responses."
    
    if 'use_rag' not in st.session_state:
        st.session_state.use_rag = True
    
    if 'model_type' not in st.session_state:
        st.session_state.model_type = "azure"
    
    if 'processed' not in st.session_state:
        st.session_state.processed = False

    if 'model_initialized' not in st.session_state:
        st.session_state.model_initialized = False


def render_sidebar():
    """Render the sidebar with all configuration options"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model Selection
        with st.container():
            render_model_selection(st.session_state.chat_manager, st.session_state)
        
        # System Prompt
        with st.container():
            render_system_prompt_selection(st.session_state)
        
        # RAG Configuration
        with st.container():
            render_rag_settings(st.session_state.chat_manager, st.session_state)
        
        # Chat Management
        with st.container():
            render_chat_management(st.session_state)
        
        # System Status
        with st.container():
            render_system_status(st.session_state, st.session_state.chat_manager)


def render_chat_interface():
    """Render the main chat interface"""
    st.subheader("💬 Chat Interface")
    
    # Display current configuration
    if st.session_state.model_initialized:
        render_chat_metrics(st.session_state)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                get_chat_message_html("user", message["content"]),
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                get_chat_message_html(
                    "assistant",
                    message["content"],
                    message.get("model", "AI"),
                    message.get("rag_used", False)
                ),
                unsafe_allow_html=True
            )
    
    # Chat input
    if st.session_state.model_initialized:
        chat_placeholder = "Ask a question..." + (
            " (RAG Enabled)" if st.session_state.use_rag and st.session_state.processed 
            else " (General Knowledge)"
        )
        
        if prompt := st.chat_input(chat_placeholder):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    try:
                        response, sources = st.session_state.chat_manager.get_response(
                            prompt, 
                            st.session_state.system_prompt, 
                            st.session_state.use_rag
                        )
                        
                        # Add assistant response to chat
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "model": st.session_state.model_type,
                            "rag_used": st.session_state.use_rag and st.session_state.processed
                        })
                        
                        st.rerun()
                        
                    except Exception as e:
                        error_msg = f"❌ Error generating response: {str(e)}"
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg
                        })
                        st.rerun()
    else:
        st.info("👈 Please initialize a model in the sidebar to start chatting.")


def main():
    """Main application entry point"""
    # Page configuration
    st.set_page_config(
        page_title="Advanced RAG Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Main header
    st.markdown(get_header_html(), unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        render_chat_interface()
    
    with col2:
        render_features_panel()


if __name__ == "__main__":
    main()