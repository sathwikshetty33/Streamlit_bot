# AI-Powered Chatbot Assistant

A customizable Streamlit-based chatbot that provides an interactive interface for websites. The chatbot uses Groq's LLM API for intelligent responses and includes voice input capabilities.

## Features

- 💬 Full-screen chat interface with modern UI
- 🎤 Voice-to-text input support
- 💡 Intelligent responses using Groq's LLM
- 🔄 Conversation history management
- 📱 Responsive design for all devices
- ⚡ Real-time message updates
- 🎯 Customizable responses and behavior

## Prerequisites

- Python 3.7+
- Groq API key
- Required Python packages

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sathwikshetty33/Streamlit-bot.git
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required packages:
```bash
pip install streamlit openai groq streamlit
```



## Configuration

1. Create a `.streamlit/secrets.toml` file:
```toml
GROQ_API_KEY = "your-groq-api-key"
```

2. Customize the bot's behavior by modifying `STORE_INFO` and `WEBSITE_INFO` in the code:
```python
STORE_INFO = """
Your store description here
"""

WEBSITE_INFO = {
    "greetings": [...],
    "fallback_responses": {...},
    "common_queries": {...}
}
```

## Running the Application

```bash
streamlit run app.py
```

## Customization

### Modifying Bot Responses

The chatbot's responses can be customized by modifying:

1. `STORE_INFO`: Contains the main store description
2. `WEBSITE_INFO`: Contains structured responses for:
   - Greetings
   - Fallback responses
   - Common queries
   - Error messages

### Styling

The chatbot's appearance can be customized by modifying the CSS in the `main()` function:
- Colors
- Fonts
- Layout
- Animations
- Message bubble styles

### Chat Behavior

Modify the following functions to customize the chat behavior:
- `get_bot_response()`: Change how the bot generates responses
- `get_fallback_response()`: Modify fallback behavior
- `handle_input()`: Customize input processing
- `convert_audio_to_text()`: Adjust voice input settings

## Dependencies

- streamlit
- openai
- groq
- SpeechRecognition
- audio-recorder-streamlit
- pyaudio
- pandas
- numpy

## System Requirements

- RAM: 4GB minimum (8GB recommended)
- Storage: 500MB free space
- Processor: 1.6GHz or faster
- Internet connection required
- Microphone (for voice input)


## Acknowledgments

- Thanks to Groq for providing the LLM API
- Streamlit for the web framework



