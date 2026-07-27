# 📚 PDF RAG & Roadmap Summarizer

A complete, production-ready application that reads any PDF file, generates an executive summary and structured learning/action roadmap using **LangChain Map-Reduce**, and allows interactive Q&A over the PDF using **RAG (Retrieval-Augmented Generation)** with page-level citations.

---

## 🛠️ Tech Stack & Architecture

- **Orchestration**: LangChain (`langchain`, `langchain-community`, `langchain-openai`)
- **PDF Extraction & Chunking**: `PyPDFLoader` & `RecursiveCharacterTextSplitter`
- **Embeddings & LLM**: OpenAI `text-embedding-3-small` & `gpt-4o-mini`
- **Vector Database**: `ChromaDB`
- **User Interface**: Streamlit

---

## 🚀 Quick Start Guide

### 1. Navigate to Project Directory
```bash
cd D:\Program\Projects\pdf-rag-summarizer
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
Create a `.env` file in the project folder:
```env
OPENAI_API_KEY=your_actual_openai_api_key
```

### 5. Launch Application
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
D:\Program\Projects\pdf-rag-summarizer\
├── app.py              # Streamlit Web App UI
├── pdf_processor.py    # PDF loading & text splitting
├── vector_store.py     # ChromaDB vector embedding manager
├── summarizer.py       # Map-Reduce summary & roadmap generator
├── rag_chain.py        # Conversational RAG retrieval chain
├── config.py           # Application settings & constants
├── requirements.txt    # Project Python dependencies
├── .env.example        # Environment variable template
└── README.md           # Documentation
```
