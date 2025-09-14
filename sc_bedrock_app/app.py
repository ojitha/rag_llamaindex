import streamlit as st
import os
import sys
import tempfile
import shutil
from typing import Dict, Any

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.embeddings.bedrock import BedrockEmbedding
from llama_index.llms.bedrock_converse import BedrockConverse

# Data folder is now local to this application

# Page configuration
st.set_page_config(
    page_title="Science Community Chat",
    page_icon="🔬",
    layout="wide"
)

st.title("☁️ Science Community Chat Engine - Bedrock")
st.markdown("*Chat with historical science documents using AWS Bedrock models and LlamaIndex chat engines*")

@st.cache_resource
def load_documents(data_path: str):
    """Load documents from the specified data directory"""
    try:
        if not os.path.exists(data_path):
            st.error(f"Data path does not exist: {data_path}")
            return None
        documents = SimpleDirectoryReader(data_path).load_data()
        if not documents:
            st.error(f"No documents found in: {data_path}")
            return None
        return documents
    except Exception as e:
        st.error(f"Error loading documents: {e}")
        return None

@st.cache_resource
def create_index(documents, temperature=0.3):
    """Create the vector index with specified temperature"""
    if documents is None:
        return None

    # Initialize Bedrock LLM and embedding model
    llm = BedrockConverse(
        model="amazon.nova-pro-v1:0",
        temperature=temperature,
        max_tokens=3000
    )
    embed_model = BedrockEmbedding(
        model_name="amazon.titan-embed-text-v2:0"
    )

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
        custom_llm = BedrockConverse(
            model="amazon.nova-pro-v1:0",
            temperature=config.get("temperature", 0.3),
            max_tokens=3000
        )
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

        # Data path input
        st.subheader("📁 Data Source")

        # Directory selection method
        path_method = st.radio(
            "Choose data source method:",
            ["Use default data folder", "Enter custom path", "Upload files"],
            help="Select how you want to provide documents"
        )

        if path_method == "Use default data folder":
            data_path = os.path.join(os.path.dirname(__file__), "data")
            st.info(f"Using default path: `{data_path}`")

        elif path_method == "Enter custom path":
            default_data_path = os.path.join(os.path.dirname(__file__), "data")
            data_path = st.text_input(
                "Data Directory Path",
                value=default_data_path,
                help="Enter the full path to directory containing documents",
                placeholder="/path/to/your/documents"
            )

            # Add browse button hint
            st.info("💡 **Tip**: You can copy the path from your file manager")

            # Show some common paths as examples
            with st.expander("📂 Example paths"):
                st.text("macOS: /Users/username/Documents/my_docs")
                st.text("Windows: C:\\Users\\username\\Documents\\my_docs")
                st.text("Linux: /home/username/documents/my_docs")

        else:  # Upload files
            st.info("📂 **Visual File Selection**")

            # Create columns for better layout
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("### 📁 Select Your Documents")
                st.markdown("*Drag and drop files or click to browse*")

                uploaded_files = st.file_uploader(
                    "📎 Choose Document Files",
                    accept_multiple_files=True,
                    type=['txt', 'md', 'pdf', 'docx'],
                    help="Select all files from your directory at once",
                    label_visibility="collapsed"
                )

            with col2:
                st.markdown("### 📊 File Stats")
                if uploaded_files:
                    st.metric("Files Selected", len(uploaded_files))

                    # Show file types
                    file_types = {}
                    for f in uploaded_files:
                        ext = f.name.split('.')[-1].lower()
                        file_types[ext] = file_types.get(ext, 0) + 1

                    st.markdown("**File Types:**")
                    for ext, count in file_types.items():
                        st.text(f"📄 {ext.upper()}: {count}")
                else:
                    st.metric("Files Selected", 0)

            # Visual feedback section
            if uploaded_files:
                st.markdown("---")
                st.markdown("### 📋 Selected Files")

                # Create expandable file list
                with st.expander(f"📁 View {len(uploaded_files)} selected files", expanded=len(uploaded_files) <= 5):
                    for i, uploaded_file in enumerate(uploaded_files, 1):
                        file_size = len(uploaded_file.getvalue()) / 1024  # KB
                        st.text(f"{i:2d}. 📄 {uploaded_file.name} ({file_size:.1f} KB)")

                # Create temp directory for uploaded files
                if 'temp_dir' not in st.session_state:
                    st.session_state.temp_dir = tempfile.mkdtemp()

                # Save uploaded files to temp directory
                temp_dir = st.session_state.temp_dir

                # Clear previous files
                try:
                    for file in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                except Exception:
                    pass  # Ignore errors when clearing temp files

                # Save new files
                for uploaded_file in uploaded_files:
                    with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())

                data_path = temp_dir
                st.success(f"✅ Ready to process {len(uploaded_files)} documents!")

                # Show processing info
                st.info("💡 **Tip**: These files will be processed into searchable chunks for the chat engine.")

            else:
                # Show upload instructions
                st.markdown("---")
                st.markdown("### 📝 How to Upload")
                st.markdown("""
                **Option 1 - Drag & Drop:**
                - Drag files from your file manager directly onto the upload area above

                **Option 2 - Browse:**
                - Click the upload area to open file browser
                - Select multiple files using Ctrl+Click (Windows/Linux) or Cmd+Click (Mac)
                - Choose files from the same directory for best results

                **Supported Formats:**
                - 📄 Text files (.txt)
                - 📝 Markdown (.md)
                - 📖 PDF documents (.pdf)
                - 📃 Word documents (.docx)
                """)

                # Fallback to default if no files uploaded
                data_path = os.path.join(os.path.dirname(__file__), "data")
                st.warning("⚠️ No files selected. Using default sample documents.")

        st.divider()

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
        st.subheader("📚 Current Data Path")
        st.info(f"Documents loaded from: `{data_path}`")

        # Show available files if path exists
        if os.path.exists(data_path):
            try:
                files = [f for f in os.listdir(data_path) if f.endswith(('.txt', '.md', '.pdf', '.docx'))]
                if files:
                    st.text("Available documents:")
                    for file in sorted(files)[:10]:  # Show first 10 files
                        st.text(f"• {file}")
                    if len(files) > 10:
                        st.text(f"... and {len(files) - 10} more files")
                else:
                    st.warning("No supported document files found in directory")
            except Exception as e:
                st.error(f"Error reading directory: {e}")
        else:
            st.error("Directory does not exist")

    # Main chat interface
    st.header(f"💬 Chat ({engine_type.replace('_', ' ').title()})")

    # Load documents and create index
    with st.spinner("Loading documents and creating index..."):
        documents = load_documents(data_path)
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