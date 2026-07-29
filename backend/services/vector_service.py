from typing import List, Dict
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
import config

# In-Memory cache for BM25 retrievers per collection ID
_BM25_CACHE: Dict[str, BM25Retriever] = {}

class VectorService:
    """Vector embedding, ChromaDB storage, and Hybrid BM25+Vector search service."""
    
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
        
        # Build BM25 keyword index for exact keyword search
        try:
            bm25 = BM25Retriever.from_documents(chunks)
            bm25.k = 6
            _BM25_CACHE[collection_name] = bm25
        except Exception as e:
            print(f"[VectorService] BM25 indexing warning: {e}")
            
        return vector_store

    @classmethod
    def get_collection(cls, collection_name: str, api_key: str = None) -> Chroma:
        embeddings = cls.get_embeddings(api_key)
        return Chroma(
            persist_directory=config.VECTOR_STORE_DIR,
            embedding_function=embeddings,
            collection_name=collection_name
        )

    @classmethod
    def get_bm25_retriever(cls, collection_name: str, chunks: List[Document] = None) -> BM25Retriever:
        if collection_name in _BM25_CACHE:
            return _BM25_CACHE[collection_name]
        if chunks:
            bm25 = BM25Retriever.from_documents(chunks)
            bm25.k = 6
            _BM25_CACHE[collection_name] = bm25
            return bm25
        return None
