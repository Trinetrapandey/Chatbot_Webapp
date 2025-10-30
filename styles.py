"""
UI Styling Module
Contains all CSS styling for the Streamlit application
"""

CUSTOM_CSS = """
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    .chat-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 0 15px;
        margin: 0.5rem 0;
        margin-left: 3rem;
    }
    .chat-assistant {
        background: #f1f3f4;
        padding: 1rem;
        border-radius: 15px 15px 15px 0;
        margin: 0.5rem 0;
        margin-right: 3rem;
        border-left: 4px solid #667eea;
    }
    .model-badge {
        background: #e5e7eb;
        padding: 0.25rem 0.5rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .rag-badge {
        background: #10b981;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .stButton button {
        width: 100%;
    }
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
</style>
"""

def get_header_html():
    """Return the main header HTML"""
    return """
    <div class="main-header">
        <h1>🤖 Advanced RAG Chatbot with Pinecone</h1>
        <p>Multi-model AI assistant with document intelligence and custom prompts</p>
    </div>
    """

def get_feature_card_html(title, description):
    """Generate a feature card HTML"""
    return f"""
    <div class="feature-card">
        <h4>{title}</h4>
        <p>{description}</p>
    </div>
    """

def get_chat_message_html(role, content, model=None, rag_used=False):
    """Generate chat message HTML"""
    if role == "user":
        return f'<div class="chat-user"><strong>You:</strong><br>{content}</div>'
    else:
        model_badge = f'<span class="model-badge">{model.upper()}</span>' if model else ''
        rag_badge = '<span class="rag-badge">RAG</span>' if rag_used else ''
        
        return f'''<div class="chat-assistant">
            <strong>Assistant:</strong>{model_badge}{rag_badge}<br>
            {content}
        </div>'''