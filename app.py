"""
RAG-based AI Teaching Assistant - Streamlit Web Application
Main entry point for the web interface
"""
import streamlit as st
import os
from rag_core import RAGAssistant

# Page configuration
st.set_page_config(
    page_title="RAG AI Teaching Assistant",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'rag_assistant' not in st.session_state:
    try:
        embeddings_path = os.getenv('EMBEDDINGS_PATH', 'embeddings.joblib')
        st.session_state.rag_assistant = RAGAssistant(embeddings_path)
        st.session_state.initialized = True
    except Exception as e:
        st.error(f"Failed to initialize RAG assistant: {str(e)}")
        st.session_state.initialized = False
        st.session_state.rag_assistant = None

# Header
st.title("🎓 RAG AI Teaching Assistant")
st.markdown("Ask questions about your course content and get guided to the relevant video sections!")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # LLM Provider Selection
    llm_provider = st.selectbox(
        "LLM Provider",
        ["Ollama (Local)", "OpenAI", "Anthropic"],
        index=0
    )
    
    if llm_provider == "Ollama (Local)":
        ollama_url = st.text_input("Ollama URL", value=os.getenv("OLLAMA_URL", "http://localhost:11434"))
        embedding_model = st.text_input("Embedding Model", value=os.getenv("EMBEDDING_MODEL", "bge-m3"))
        llm_model = st.text_input("LLM Model", value=os.getenv("LLM_MODEL", "llama3.2"))
    elif llm_provider == "OpenAI":
        openai_api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        embedding_model = st.selectbox("Embedding Model", ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"])
        llm_model = st.selectbox("LLM Model", ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"])
    else:  # Anthropic
        anthropic_api_key = st.text_input("Anthropic API Key", type="password", value=os.getenv("ANTHROPIC_API_KEY", ""))
        embedding_model = st.selectbox("Embedding Model", ["text-embedding-3-small", "text-embedding-3-large"])
        llm_model = st.selectbox("LLM Model", ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"])
    
    top_results = st.slider("Number of top results", min_value=3, max_value=10, value=5)
    
    st.markdown("---")
    st.markdown("### 📊 Status")
    if st.session_state.initialized:
        st.success("✅ RAG Assistant Ready")
        if st.session_state.rag_assistant:
            df = st.session_state.rag_assistant.df
            st.info(f"📚 Loaded {len(df)} chunks from embeddings")

# Main content area
if not st.session_state.initialized:
    st.warning("⚠️ Please ensure embeddings.joblib file exists in the project root.")
    st.stop()

# Query input
query = st.text_input(
    "💬 Ask a question about the course:",
    placeholder="e.g., Where is HTML concluded in this course?"
)

if st.button("🔍 Search", type="primary") or query:
    if not query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("🔍 Searching and generating response..."):
            try:
                # Update RAG assistant configuration
                if llm_provider == "Ollama (Local)":
                    st.session_state.rag_assistant.set_ollama_config(ollama_url, embedding_model, llm_model)
                elif llm_provider == "OpenAI":
                    if not openai_api_key:
                        st.error("Please provide OpenAI API Key")
                        st.stop()
                    st.session_state.rag_assistant.set_openai_config(openai_api_key, embedding_model, llm_model)
                else:  # Anthropic
                    if not anthropic_api_key:
                        st.error("Please provide Anthropic API Key")
                        st.stop()
                    st.session_state.rag_assistant.set_anthropic_config(anthropic_api_key, embedding_model, llm_model)
                
                # Get response
                response, relevant_chunks = st.session_state.rag_assistant.query(query, top_k=top_results)
                
                # Display response
                st.markdown("### 📝 Answer")
                st.markdown(response)
                
                # Display relevant chunks
                if relevant_chunks is not None and len(relevant_chunks) > 0:
                    st.markdown("### 📹 Relevant Video Sections")
                    for idx, chunk in relevant_chunks.iterrows():
                        with st.expander(f"Video {chunk['number']}: {chunk['title']} (Time: {int(chunk['start'])}s - {int(chunk['end'])}s)"):
                            st.write(f"**Text:** {chunk['text']}")
                            st.write(f"**Start:** {chunk['start']:.2f}s | **End:** {chunk['end']:.2f}s")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("### ℹ️ About")
st.markdown("""
This RAG (Retrieval-Augmented Generation) assistant helps you find relevant content in your course videos.
It uses semantic search to find the most relevant video sections and generates contextual answers.
""")

