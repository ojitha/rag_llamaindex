# RAG with LlamaIndex - Science Community Chat

A comprehensive Retrieval-Augmented Generation (RAG) project using LlamaIndex with AWS Bedrock integration for AI-powered science community content analysis. This project demonstrates various RAG techniques through Jupyter notebooks focused on scientific documents about historical figures like Albert Einstein and Marie Curie.

## Main Features

### 🚀 Interactive Streamlit Application
The `sc_app/` directory contains a production-ready web interface that provides:

- **Multiple Chat Engine Testing**: Switch between Condense Question, Context, and Condense+Context modes
- **Real-time Configuration**: Adjust temperature, memory token limits, and custom prompts
- **Clean Chat Interface**: Intuitive conversation experience with message history
- **Self-contained**: Includes its own data folder for easy deployment

### 📚 Science Community Chat Notebook
The primary notebook `Science_Community/2025-09-12-LlamaIndexScienceCommunityChat.ipynb` demonstrates:

- **Complete RAG Architecture**: Document ingestion, chunking, indexing, and querying
- **Multiple Chat Engine Modes**: Condense Question, Context Chat, and hybrid approaches
- **Comprehensive Evaluation**: Hit Rate, MRR, Faithfulness, and Relevancy metrics
- **Interactive Science Conversations**: Chat with AI about Einstein and Marie Curie using scientific documents

### ☁️ AWS Bedrock Integration
The `2025-09-12-LlamaBedRock.ipynb` notebook shows:
- AWS Bedrock embeddings and LLM integration
- Cloud-based RAG deployment patterns

## Quick Start

### Option 1: Interactive Streamlit App (Recommended)
Experience the chat engines through a user-friendly web interface:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Launch the Streamlit app
cd sc_app
./run_app.sh
```

The app provides:
- **Chat Engine Selection**: Test different modes (Condense Question, Context, Condense+Context)
- **Real-time Configuration**: Adjust temperature, memory limits, and prompts
- **Interactive Q&A**: Chat with the science documents through a clean interface

### Option 2: Jupyter Notebooks
For detailed exploration and learning:

```bash
# Install dependencies using uv package manager
uv sync

# Launch Jupyter
uv run jupyter lab
```

### Prerequisites
- Python 3.12+
- OpenAI API key (for notebooks and Streamlit app)
- AWS credentials (for Bedrock integration notebook)


## Project Structure

```
├── Science_Community/                    # Main notebook directory
│   ├── 2025-09-12-LlamaIndexScienceCommunityChat.ipynb  # Primary RAG demonstration
│   ├── 2025-09-12-LlamaBedRock.ipynb    # AWS Bedrock integration
│   └── data/                            # Scientific documents
│       ├── AlbertEinstein.txt
│       ├── MarieCurie.txt
│       ├── friends.txt
│       └── meetingMarieAlbert.txt
├── sc_app/                              # Streamlit application
│   ├── app.py                           # Main application
│   ├── data/                            # Local copy of documents
│   ├── README.md                        # App-specific documentation
│   └── run_app.sh                       # Launch script
└── pyproject.toml                       # Project dependencies
```

## Key Technologies

- **LlamaIndex**: Core RAG framework for document indexing and querying
- **OpenAI**: GPT models and embeddings for language generation
- **AWS Bedrock**: Cloud-based LLM and embedding services
- **Streamlit**: Interactive web application framework
- **Jupyter**: Interactive notebook environment
- **uv**: Fast Python package manager

## What You'll Learn

### RAG Fundamentals
- Document loading with `SimpleDirectoryReader`
- Text chunking strategies using `TokenTextSplitter`
- Vector indexing with `VectorStoreIndex`
- Summary indexing with `SummaryIndex`

### Advanced Chat Patterns
- **Condense Question Engine**: Reformulates queries with conversation history
- **Context Chat Engine**: Direct context-based responses
- **Memory Management**: Conversation state handling

### Evaluation & Quality Assurance
- **Retrieval Metrics**: Hit Rate and Mean Reciprocal Rank (MRR)
- **Response Quality**: Faithfulness and Relevancy evaluation
- **Hallucination Detection**: Systematic verification against source material

## Usage Examples

Both the Streamlit app and notebooks support practical conversations like:
- "Tell me about Einstein's theory of relativity"
- "How did Marie Curie discover radium?"
- "What was the relationship between Einstein and Marie Curie?"
- "Compare Einstein and Marie Curie's scientific approaches"

### Streamlit App Benefits
- **Instant Testing**: No code required - just select options and chat
- **Configuration Comparison**: Easily switch between chat engines and settings
- **User-Friendly**: Perfect for non-technical users to explore RAG capabilities

### Notebook Benefits
- **Deep Learning**: Understand the implementation details and evaluation metrics
- **Customization**: Modify code, add new features, or experiment with different models
- **Analysis**: Each query shows retrieval chunks and evaluation scores