# RAG with LlamaIndex - Science Community Chat

A comprehensive Retrieval-Augmented Generation (RAG) project using LlamaIndex with AWS Bedrock integration for AI-powered science community content analysis. This project demonstrates various RAG techniques through Jupyter notebooks focused on scientific documents about historical figures like Albert Einstein and Marie Curie.

## Main Features

### Science Community Chat Notebook
The primary notebook `Science_Community/2025-09-12-LlamaIndexScienceCommunityChat.ipynb` demonstrates:

- **Complete RAG Architecture**: Document ingestion, chunking, indexing, and querying
- **Multiple Chat Engine Modes**: Condense Question, Context Chat, and hybrid approaches
- **Comprehensive Evaluation**: Hit Rate, MRR, Faithfulness, and Relevancy metrics
- **Interactive Science Conversations**: Chat with AI about Einstein and Marie Curie using scientific documents

### AWS Bedrock Integration
The `2025-09-12-LlamaBedRock.ipynb` notebook shows:
- AWS Bedrock embeddings and LLM integration
- Cloud-based RAG deployment patterns

## Quick Start

### Environment Setup
```bash
# Install dependencies using uv package manager
uv sync

# Activate virtual environment
source .venv/bin/activate

# Launch Jupyter
uv run jupyter lab
```

### Prerequisites
- Python 3.12+
- OpenAI API key (for main notebook)
- AWS credentials (for Bedrock integration)


## Key Technologies

- **LlamaIndex**: Core RAG framework for document indexing and querying
- **OpenAI**: GPT models and embeddings for language generation
- **AWS Bedrock**: Cloud-based LLM and embedding services
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

The notebooks demonstrate practical conversations like:
- "Tell me about Einstein's theory of relativity"
- "How did Marie Curie discover radium?"
- "What was the relationship between Einstein and Marie Curie?"

Each query retrieves relevant document chunks and generates contextually accurate responses with evaluation metrics.