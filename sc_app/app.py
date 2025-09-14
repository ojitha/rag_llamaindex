import streamlit as st
import os
import sys
from typing import Dict, Any

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

# Data folder is now local to this application

# Page configuration
st.set_page_config(
    page_title="Science Community Chat",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Science Community Chat Engine")
st.markdown("*Chat with historical science documents using different LlamaIndex chat engines*")

@st.cache_resource
def load_documents():
    """Load documents from the local data directory"""
    data_path = os.path.join(os.path.dirname(__file__), "data")
    try:
        documents = SimpleDirectoryReader(data_path).load_data()
        return documents
    except Exception as e:
        st.error(f"Error loading documents: {e}")
        return None

@st.cache_resource
def create_index(documents, temperature=0.3):
    """Create the vector index with specified temperature"""
    if documents is None:
        return None

    # Initialize LLM and embedding model
    llm = OpenAI(model="gpt-4o", temperature=temperature)
    embed_model = OpenAIEmbedding()

    # Set global settings
    Settings.llm = llm
    Settings.embed_model = embed_model

    # Create index
    index = VectorStoreIndex.from_documents(documents)
    return index

def create_chat_engine(index, engine_type: str, config: Dict[str, Any]):
    """Create chat engine based on type and configuration"""
    if index is None:
        return None

    if engine_type == "condense_question":
        return index.as_chat_engine("condense_question", verbose=True)

    elif engine_type == "context":
        memory = ChatMemoryBuffer.from_defaults(
            token_limit=config.get("token_limit", 3900)
        )
        return index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            system_prompt=config.get("system_prompt",
                "You are familiar with biographies of Albert and Marie, as well as their professional and social friendships and relationships.")
        )

    elif engine_type == "condense_plus_context":
        memory = ChatMemoryBuffer.from_defaults(
            token_limit=config.get("token_limit", 3900)
        )
        # Use custom LLM if temperature is different
        custom_llm = OpenAI(model="gpt-4o", temperature=config.get("temperature", 0.3))
        return index.as_chat_engine(
            chat_mode="condense_plus_context",
            memory=memory,
            llm=custom_llm,
            context_prompt=config.get("context_prompt",
                "You are familiar with biographies of Albert and Marie, as well as their professional and social friendships and relationships."),
            verbose=True
        )

    else:
        return index.as_chat_engine()

def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Chat engine selection
        engine_type = st.selectbox(
            "Chat Engine",
            ["condense_question", "context", "condense_plus_context"],
            help="""
            • **condense_question**: Condenses conversation history into standalone questions
            • **context**: Uses explicit memory management with retrieved context
            • **condense_plus_context**: Hybrid approach combining both strategies
            """
        )

        st.divider()

        # Common settings
        st.subheader("🌡️ Common Settings")
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Controls randomness in responses. Lower = more focused, Higher = more creative"
        )

        # Engine-specific settings
        st.subheader("🔧 Engine-Specific Settings")

        config = {"temperature": temperature}

        if engine_type in ["context", "condense_plus_context"]:
            token_limit = st.number_input(
                "Memory Token Limit",
                min_value=1000,
                max_value=8000,
                value=3900,
                step=100,
                help="Maximum tokens to keep in conversation memory"
            )
            config["token_limit"] = token_limit

            if engine_type == "context":
                system_prompt = st.text_area(
                    "System Prompt",
                    value="You are familiar with biographies of Albert and Marie, as well as their professional and social friendships and relationships.",
                    height=100,
                    help="Instructions for the AI about its role and knowledge"
                )
                config["system_prompt"] = system_prompt

            elif engine_type == "condense_plus_context":
                context_prompt = st.text_area(
                    "Context Prompt",
                    value="You are familiar with biographies of Albert and Marie, as well as their professional and social friendships and relationships.",
                    height=100,
                    help="Instructions for how to use the retrieved context"
                )
                config["context_prompt"] = context_prompt

        # Data info
        st.divider()
        st.subheader("📚 Data Source")
        st.info("Documents loaded from: `./data/`")
        data_files = [
            "AlbertEinstein.txt",
            "MarieCurie.txt",
            "friends.txt",
            "meetingMarieAlbert.txt"
        ]
        for file in data_files:
            st.text(f"• {file}")

    # Main chat interface
    st.header(f"💬 Chat ({engine_type.replace('_', ' ').title()})")

    # Load documents and create index
    with st.spinner("Loading documents and creating index..."):
        documents = load_documents()
        if documents:
            index = create_index(documents, temperature)
            if index:
                chat_engine = create_chat_engine(index, engine_type, config)
            else:
                st.error("Failed to create index")
                return
        else:
            st.error("Failed to load documents")
            return

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the science community..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = chat_engine.chat(prompt)
                    response_text = str(response)
                    st.markdown(response_text)

                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

                except Exception as e:
                    error_msg = f"Error generating response: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Clear chat button
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()