import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI
import time
from groq import Groq
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import io
import wave
import numpy as np
STORE_INFO = """
Indeify is an ecommerce store specializing in handicrafts. We offer a unique selection of handcrafted items 
that celebrate artisanal skills and traditional craftsmanship.
"""

WEBSITE_INFO = {
    "greetings": [
        "Hello! Welcome to Indeify. How can I help you today?",
        "Hi there! Welcome to Indeify's handicraft store. What can I assist you with?",
        "Welcome to Indeify! How may I assist you with our handicraft collection?"
    ],
    "fallback_responses": {
        "greeting": [
            "Hi! Welcome to Indeify. How can I assist you today?",
            "Hello! I'm here to help you explore Indeify's handicraft collection. What would you like to know?",
            "Welcome to Indeify! How can I help you with our handicrafts?"
        ],
        "general": [
            "At Indeify, we offer unique handicrafts. You can ask me about our products, services, or any other features.",
            "I can help you explore Indeify's handicraft collection, assist with navigation, or answer questions about our services.",
            "Feel free to ask about our handicrafts, services, or any other aspects of Indeify!"
        ],
        "error": [
            "I'm here to help you with Indeify's handicraft collection! Could you please rephrase your question?",
            "I want to help you better explore our handicrafts. Could you provide more details?",
            "Let me assist you better with finding the perfect handicraft. Could you be more specific?"
        ]
    },
    "common_queries": {
        "hello": ["Hi there!", "Hello!", "Welcome to Indeify!"],
        "help": ["I can help you with:",
                "- Exploring our handicraft collection",
                "- Account management",
                "- Navigation assistance",
                "- Order tracking",
                "- Customer support"],
        "products": ["You can explore our handicrafts by:",
                    "- Browsing categories",
                    "- Using the search bar",
                    "- Checking featured items",
                    "- Viewing special offers"],
        "contact": ["You can reach Indeify through:",
                   "- Live chat",
                   "- Email: support@indeify.com",
                   "- Contact form on our website"]
    }
}
def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! Welcome to Indeify. I'm your personal shopping assistant. How can I help you explore our unique handicraft collection today?"}
        ]
        
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
        
    # Initialize Groq client with API key
    if 'groq_client' not in st.session_state:
        try:
            api_key = st.secrets["GROQ_API_KEY"]  # Get API key from Streamlit secrets
            st.session_state.groq_client = Groq(api_key=api_key)
            st.session_state.groq_initialized = True
        except Exception as e:
            st.session_state.groq_client = None
            st.session_state.groq_initialized = False
            st.error(f"Error initializing Groq client: {str(e)}")
            
    if 'last_error' not in st.session_state:
        st.session_state.last_error = None

def get_bot_response(user_input):
    """Get response with conversation history context"""
    if not st.session_state.groq_initialized:
        st.error("Groq client not initialized. Please check your API key.")
        return get_fallback_response(user_input)
        
    try:
        messages = [
            {"role": "system", "content": f"""You are website assistant. You help customers with our handicraft e-commerce store.
            
            Key Information:
            {STORE_INFO}
            
            Instructions:
            - Always mention we are Indeify when introducing our store
            - Be concise, friendly, and direct in your responses
            - Focus on handicrafts and artisanal products
            - If asked about products, mention we specialize in handicrafts
            - Keep responses under 3 sentences unless more detail is needed
            - Maintain conversation context and refer to previous messages when relevant
            - Remember user's name and other details they share"""}
        ]
        
        for msg in st.session_state.messages[-5:]:
            messages.append({
                "role": "user" if msg["role"] == "user" else "assistant",
                "content": msg["content"]
            })
            
        messages.append({"role": "user", "content": user_input})

        response = st.session_state.groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Groq's model
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
        return get_fallback_response(user_input)
    

def get_fallback_response(user_input):
    user_input = user_input.lower()
    
    # Check for website name questions
    if any(word in user_input for word in ['website', 'store', 'shop', 'name']):
        return "Our store is called Indeify, and we specialize in beautiful handicrafts. Would you like to know more about our products?"
    
    # Check for common greetings
    if any(word in user_input for word in ['hello', 'hi', 'hey', 'greetings']):
        return WEBSITE_INFO["fallback_responses"]["greeting"][0]
    
    # Rest of the function remains the same...
    if 'help' in user_input:
        return "\n".join(WEBSITE_INFO["common_queries"]["help"])
    
    if any(word in user_input for word in ['product', 'item', 'buy', 'purchase', 'handicraft']):
        return "\n".join(WEBSITE_INFO["common_queries"]["products"])
    
    if any(word in user_input for word in ['contact', 'support', 'help', 'reach']):
        return "\n".join(WEBSITE_INFO["common_queries"]["contact"])
    
    return WEBSITE_INFO["fallback_responses"]["general"][0]

def handle_input():
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # Get bot response
        bot_response = get_bot_response(user_message)
        
        # Add bot response to chat
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Save to chat history
        st.session_state.chat_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_message": user_message,
            "bot_response": bot_response
        })
        
        # Clear input
        st.session_state.user_input = ""
import streamlit as st
# ... (previous imports remain the same)

def main():
    st.set_page_config(
        page_title="Website Assistant",
        page_icon="💬",
        initial_sidebar_state="collapsed",
        layout="wide"
    )
    
    initialize_session_state()
    
    # Updated CSS for floating chat widget
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 400px;
        max-width: 90vw;
        height: 600px;
        max-height: 90vh;
        background: transparent;
        z-index: 1000;
    }

    /* Chat widget container */
    .chat-widget {
        position: relative;
        width: 100%;
        height: 100%;
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    /* Header styling */
    .chat-header {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        padding: 15px;
        font-size: 1.2em;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    /* Messages container */
    .chat-container {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background: #f5f7fa;
    }

    /* Message bubbles */
    .user-message {
        background: #2196F3;
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        float: right;
        clear: both;
        word-wrap: break-word;
        box-shadow: 0 2px 5px rgba(33,150,243,0.2);
        animation: slideInRight 0.3s ease;
    }

    .bot-message {
        background: white;
        color: #333;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        float: left;
        clear: both;
        word-wrap: break-word;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        animation: slideInLeft 0.3s ease;
    }

    /* Input container */
    .input-container {
        padding: 15px;
        background: white;
        border-top: 1px solid #eee;
    }

    /* Input field */
    .stTextInput>div>div>input {
        border-radius: 25px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 8px 15px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #2196F3 !important;
        box-shadow: 0 2px 8px rgba(33,150,243,0.2) !important;
    }

    /* Animations */
    @keyframes slideInRight {
        from { transform: translateX(100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideInLeft {
        from { transform: translateX(-100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    /* Timestamp */
    .timestamp {
        font-size: 11px;
        color: #999;
        margin: 4px 0;
        clear: both;
        text-align: center;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main {
            width: 100%;
            height: 100%;
            bottom: 0;
            right: 0;
            border-radius: 0;
        }
        
        .chat-widget {
            border-radius: 0;
        }
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    # Main chat interface
    main_container = st.container()
    
    with main_container:
        st.markdown('<div class="chat-widget">', unsafe_allow_html=True)
        
        # Chat header
        st.markdown('''
            <div class="chat-header">
                <span>💬 Indeify Assistant</span>
            </div>
        ''', unsafe_allow_html=True)
        
        # Chat messages
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(
                        f'<div class="user-message">{message["content"]}</div>'
                        f'<div class="timestamp">{datetime.now().strftime("%H:%M")}</div>', 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="bot-message">{message["content"]}</div>'
                        f'<div class="timestamp">{datetime.now().strftime("%H:%M")}</div>', 
                        unsafe_allow_html=True
                    )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Input field
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        st.text_input(
            label="Message",
            key="user_input",
            placeholder="Type your message here...",
            on_change=handle_input,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()