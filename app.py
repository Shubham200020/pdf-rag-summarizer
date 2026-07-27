import os
import streamlit as st
import config
from pdf_processor import PDFProcessor
from vector_store import VectorStoreManager
from summarizer import PDFSummarizer
from rag_chain import RAGEngine

st.set_page_config(
    page_title="PDF RAG & Roadmap Summarizer",
    page_icon="📚",
    layout="wide"
)

st.title("📚 PDF RAG & Roadmap Summarizer")
st.markdown("Upload a PDF document to generate an executive summary, extract a step-by-step roadmap, and ask questions with page-level citations.")

# Sidebar Settings
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", value=config.OPENAI_API_KEY, type="password")
model_choice = st.sidebar.selectbox("Select Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)

if not api_key:
    st.info("⚠️ Please enter your OpenAI API key in the sidebar to get started.")

# File Uploader
uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])

if uploaded_file and api_key:
    # Save uploaded file temporarily
    temp_pdf_path = os.path.join(config.TEMP_UPLOAD_DIR, uploaded_file.name)
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.sidebar.success(f"Loaded: {uploaded_file.name}")
    
    # Process PDF button or cached session state
    if "processed_pdf" not in st.session_state or st.session_state.get("pdf_name") != uploaded_file.name:
        with st.spinner("📄 Processing PDF text and building vector embeddings..."):
            # Step 1: Chunk PDF
            chunks = PDFProcessor.load_and_split(temp_pdf_path)
            st.session_state["chunks"] = chunks
            
            # Step 2: Build Vector DB
            vector_mgr = VectorStoreManager(api_key=api_key)
            vector_store = vector_mgr.create_vector_store(chunks, collection_name="user_pdf")
            st.session_state["vector_store"] = vector_store
            
            # Step 3: Summarize & Roadmap
            with st.spinner("🧠 Generating Executive Summary & Roadmap..."):
                summarizer = PDFSummarizer(api_key=api_key, model_name=model_choice)
                summary_text = summarizer.generate_summary_and_roadmap(chunks)
                st.session_state["summary_text"] = summary_text
                
            st.session_state["processed_pdf"] = True
            st.session_state["pdf_name"] = uploaded_file.name
            st.session_state["chat_history"] = []

    # Display Tabs
    tab1, tab2 = st.tabs(["📝 Summary & Roadmap", "💬 Chat with PDF (RAG)"])
    
    with tab1:
        st.subheader("📌 Summary & Actionable Roadmap")
        if "summary_text" in st.session_state:
            st.markdown(st.session_state["summary_text"])
            
    with tab2:
        st.subheader("💬 Ask Questions About the Document")
        
        # Initialize RAG Engine
        vector_store = st.session_state["vector_store"]
        rag_engine = RAGEngine(vector_store, api_key=api_key, model_name=model_choice)
        
        # Render Chat History
        for msg in st.session_state.get("chat_history", []):
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if "sources" in msg and msg["sources"]:
                    with st.expander("🔍 View Source Citations"):
                        for src in msg["sources"]:
                            st.markdown(f"**Page {src['page']}** ({src['file']}): *\"{src['snippet']}\"*")

        # Chat Input
        user_query = st.chat_input("Ask a question about your PDF...")
        if user_query:
            st.session_state["chat_history"].append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)
                
            with st.chat_message("assistant"):
                with st.spinner("Searching document..."):
                    response = rag_engine.query(user_query)
                    answer = response["answer"]
                    sources = response["sources"]
                    
                    st.write(answer)
                    if sources:
                        with st.expander("🔍 View Source Citations"):
                            for src in sources:
                                st.markdown(f"**Page {src['page']}** ({src['file']}): *\"{src['snippet']}\"*")
                                
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

else:
    st.info("👆 Upload a PDF document above to analyze.")
