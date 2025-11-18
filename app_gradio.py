import gradio as gr
from app import get_bot_response
import os

def chat_with_bot(message, history, language):
    """Chat interface for Gradio"""
    if not message.strip():
        return history
    
    # Get bot response
    bot_response = get_bot_response(message, language)
    
    # Add to history
    history.append((message, bot_response))
    
    return history

def clear_chat():
    """Clear chat history"""
    return []

# Custom CSS for better styling
custom_css = """
#chatbot {
    height: 500px;
    overflow-y: auto;
}
.title {
    text-align: center;
    font-size: 2em;
    font-weight: bold;
    color: #2E8B57;
}
.subtitle {
    text-align: center;
    font-size: 1.2em;
    color: #666;
    margin-bottom: 20px;
}
"""

with gr.Blocks(
    title="🌱 Fruitful Harvest Bot",
    theme=gr.themes.Soft(),
    css=custom_css
) as demo:
    
    # Header
    gr.Markdown(
        """
        <div class="title">🌱 Fruitful Harvest Bot</div>
        <div class="subtitle">Your personal farming guide - Ask anything about growing fruits!</div>
        """,
        elem_id="header"
    )
    
    # Language selector
    with gr.Row():
        language = gr.Dropdown(
            choices=[
                ("English", "en"),
                ("Chichewa", "ny")
            ],
            value="en",
            label="🌍 Select Language",
            interactive=True
        )
    
    # Chat interface
    chatbot = gr.Chatbot(
        label="💬 Chat with Farming Assistant",
        height=500,
        show_copy_button=True,
        elem_id="chatbot"
    )
    
    # Input area
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask about any fruit growing method... (e.g., 'How to plant mango?', 'What soil for bananas?')",
            label="Your Question",
            scale=4,
            container=False
        )
        send_btn = gr.Button("Send 🚀", variant="primary", scale=1)
        clear_btn = gr.Button("Clear 🗑️", variant="secondary", scale=1)
    
    # Examples
    gr.Examples(
        examples=[
            "How to plant mango trees?",
            "What soil is best for bananas?",
            "Pest control for guava",
            "I have clay soil, what fruits can I grow?",
            "Which fruits grow quickly?",
            "How much water does pineapple need?"
        ],
        inputs=msg,
        label="💡 Try these examples:"
    )
    
    # Event handlers
    def respond(message, chat_history, lang):
        if not message.strip():
            return "", chat_history
        
        bot_message = get_bot_response(message, lang)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    # Connect events
    msg.submit(respond, [msg, chatbot, language], [msg, chatbot])
    send_btn.click(respond, [msg, chatbot, language], [msg, chatbot])
    clear_btn.click(clear_chat, outputs=[chatbot])

# For Hugging Face Spaces
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        share=False
    )