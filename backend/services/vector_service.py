from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import config

class VectorService:
    """Vector embedding & ChromaDB storage service with automatic open-source fallback."""
    
    @staticmethod
    def get_embeddings(api_key: str = None):
        key = api_key or config.OPENAI_API_KEY
        if key and key != "your_openai_api_key_here":
            try:
                return OpenAIEmbeddings(
                    model=config.EMBEDDING_MODEL,
                    openai_api_key=key
                )
            except Exception:
                pass
                
        # Open-Source Fallback (SentenceTransformers all-MiniLM-L6-v2)
        print("[VectorService] Using HuggingFace Embeddings (all-MiniLM-L6-v2) zero-config fallback...")
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    @classmethod
    def create_collection(cls, chunks: List[Document], collection_name: str, api_key: str = None) -> Chroma:
        embeddings = cls.get_embeddings(api_key)
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=config.VECTOR_STORE_DIR,
            collection_name=collection_name
        )
        return vector_store

    @classmethod
    def get_collection(cls, collection_name: str, api_key: str = None) -> Chroma:
        embeddings = cls.get_embeddings(api_key)
        return Chroma(
            persist_directory=config.VECTOR_STORE_DIR,
            embedding_function=embeddings,
            collection_name=collection_name
        )
