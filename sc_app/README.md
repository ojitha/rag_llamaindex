# Science Community Chat App

A Streamlit application for testing different LlamaIndex chat engines with the Science Community documents.

## Features

- **Multiple Chat Engines**: Test three different chat engine types:
  - **Condense Question**: Condenses conversation history into standalone questions
  - **Context**: Uses explicit memory management with retrieved context
  - **Condense Plus Context**: Hybrid approach combining both strategies

- **Configurable Settings**:
  - Temperature control (0.0 - 1.0)
  - Memory token limit for context-based engines
  - Customizable system/context prompts

- **Interactive Interface**: Clean chat interface with conversation history

## Setup

1. **Install dependencies**:
   ```bash
   cd sc_app
   pip install -r requirements.txt
   ```

2. **Set OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Data Source

The application automatically loads documents from the local `./data/` directory, which contains:

- `AlbertEinstein.txt` - Biography of Albert Einstein
- `MarieCurie.txt` - Biography of Marie Curie
- `friends.txt` - Information about their friendships
- `meetingMarieAlbert.txt` - Meeting scenarios

## Usage

1. Select a chat engine type from the sidebar
2. Adjust temperature and engine-specific settings
3. Start chatting with questions about the scientists and their relationships
4. Compare responses between different chat engine configurations

## Example Questions

- "Tell me about Einstein's early life"
- "How did Marie Curie and Albert Einstein know each other?"
- "What were Einstein's major scientific contributions?"
- "Compare the personalities of Einstein and Marie Curie"