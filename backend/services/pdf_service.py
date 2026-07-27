import os
from typing import List, Tuple
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import config

class PDFService:
    """PDF parsing and text chunking service."""
    
    @staticmethod
    def process_pdf(pdf_path: str) -> Tuple[List[Document], int]:
        """Parses PDF and splits into chunks. Returns (chunks, total_pages)."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")
            
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        total_pages = len(pages)
        
        file_name = os.path.basename(pdf_path)
        for p in pages:
            p.metadata["source_file"] = file_name
            if "page" in p.metadata:
                p.metadata["page_label"] = p.metadata["page"] + 1

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = splitter.split_documents(pages)
        return chunks, total_pages
