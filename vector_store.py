from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import config

class VectorStoreManager:
    """Manages creation, loading, and searching of vector embeddings using ChromaDB."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.OPENAI_API_KEY
        self.embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=self.api_key
        )
    
    def create_vector_store(self, chunks: List[Document], collection_name: str = "pdf_docs") -> Chroma:
        """Embeds document chunks and stores them in Chroma vector DB."""
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=config.VECTOR_STORE_DIR,
            collection_name=collection_name
        )
        return vector_store
        
    def load_vector_store(self, collection_name: str = "pdf_docs") -> Chroma:
        """Loads an existing Chroma vector store collection."""
        return Chroma(
            persist_directory=config.VECTOR_STORE_DIR,
            embedding_function=self.embeddings,
            collection_name=collection_name
        )
