# Science Community Chat App - AWS Bedrock Edition

A Streamlit application for testing different LlamaIndex chat engines using AWS Bedrock models with customizable document sources.

## Features

- **Multiple Chat Engines**: Test three different chat engine types:
  - **Condense Question**: Condenses conversation history into standalone questions
  - **Context**: Uses explicit memory management with retrieved context
  - **Condense Plus Context**: Hybrid approach combining both strategies

- **AWS Bedrock Integration**:
  - Amazon Nova Pro LLM for text generation
  - Amazon Titan v2 embeddings for vector search
  - No OpenAI API key required

- **Configurable Settings**:
  - Temperature control (0.0 - 1.0)
  - Memory token limit for context-based engines
  - Customizable system/context prompts

- **Flexible Data Source**: Input any directory path to vectorize your own documents

- **Interactive Interface**: Clean chat interface with conversation history

## Setup

1. **Install dependencies**:
   ```bash
   cd sc_bedrock_app
   pip install -r requirements.txt
   ```

2. **Configure AWS Credentials**:
   ```bash
   # Option 1: AWS CLI
   aws configure

   # Option 2: Environment variables
   export AWS_ACCESS_KEY_ID="your-access-key"
   export AWS_SECRET_ACCESS_KEY="your-secret-key"
   export AWS_DEFAULT_REGION="us-east-1"
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Data Source

**Flexible Document Loading**: The application allows you to specify any directory path containing documents to vectorize. Supported formats include:

- `.txt` - Plain text files
- `.md` - Markdown files
- `.pdf` - PDF documents
- `.docx` - Word documents

**Default Data**: The app includes sample science community documents:
- `AlbertEinstein.txt` - Biography of Albert Einstein
- `MarieCurie.txt` - Biography of Marie Curie
- `friends.txt` - Information about their friendships
- `meetingMarieAlbert.txt` - Meeting scenarios

## Usage

1. **Choose Data Source**: Select from three convenient options:
   - **Default folder**: Use the included sample documents
   - **Custom path**: Enter any directory path containing your documents
   - **Upload files**: Drag & drop files directly into the browser
2. **Select Chat Engine**: Choose from condense question, context, or hybrid approaches
3. **Adjust Settings**: Configure temperature and engine-specific parameters
4. **Start Chatting**: Ask questions about your documents
5. **Compare Engines**: Test different configurations to see response variations

### Data Source Options

- **📁 Default Data**: Pre-loaded science community documents
- **🗂️ Custom Directory**: Point to any folder with documents (with helpful path examples)
- **📂 Visual File Upload**: Enhanced drag & drop interface with:
  - **📊 Real-time Stats**: File count and type breakdown
  - **📋 File List**: Preview of selected documents with sizes
  - **🎯 Visual Feedback**: Clear upload progress and status
  - **📝 Help Instructions**: Step-by-step guidance for file selection
  - **Multi-format Support**: .txt, .md, .pdf, .docx files

## AWS Bedrock Models Used

- **LLM**: Amazon Nova Pro (amazon.nova-pro-v1:0)
- **Embeddings**: Amazon Titan v2 (amazon.titan-embed-text-v2:0)

## Example Questions

- "Tell me about Einstein's early life"
- "How did Marie Curie and Albert Einstein know each other?"
- "What were Einstein's major scientific contributions?"
- "Compare the personalities of Einstein and Marie Curie"