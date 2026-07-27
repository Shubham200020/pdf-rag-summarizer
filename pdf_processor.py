import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP

class PDFProcessor:
    """Handles PDF loading, text extraction, and chunking."""
    
    @staticmethod
    def load_and_split(pdf_path: str) -> List[Document]:
        """Loads a PDF file and splits it into chunked Document objects with metadata."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at path: {pdf_path}")
            
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        # Add filename metadata to each document page
        file_name = os.path.basename(pdf_path)
        for doc in documents:
            doc.metadata["source_file"] = file_name
            # Ensure page numbers are 1-indexed for clear user feedback
            if "page" in doc.metadata:
                doc.metadata["page_label"] = doc.metadata["page"] + 1

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = splitter.split_documents(documents)
        return chunks
