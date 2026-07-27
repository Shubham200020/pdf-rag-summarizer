import os
from typing import List, Tuple
from pypdf import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import config

class PDFService:
    """PDF parsing, chunking, and pre-embedding audit validation service."""
    
    @staticmethod
    def audit_pdf(pdf_path: str, file_size: int) -> Tuple[bool, str]:
        """Audits PDF file against size, encryption, page count, and text extractability constraints."""
        # 1. File Size Audit
        if file_size == 0:
            return False, "Uploaded PDF file is empty (0 bytes)."
            
        if file_size > config.MAX_FILE_SIZE_BYTES:
            size_mb = round(file_size / (1024 * 1024), 2)
            return False, f"PDF file size ({size_mb} MB) exceeds maximum allowed limit of {config.MAX_FILE_SIZE_MB} MB."
            
        # 2. Open PDF and check structure
        try:
            reader = PdfReader(pdf_path)
        except Exception as e:
            return False, f"Corrupted or invalid PDF structure: {str(e)}"
            
        # 3. Encryption / Password Check
        if reader.is_encrypted:
            return False, "PDF is password-protected or encrypted. Please remove password protection before uploading."
            
        # 4. Page Count Limit Check
        total_pages = len(reader.pages)
        if total_pages == 0:
            return False, "PDF contains 0 pages."
            
        if total_pages > config.MAX_PAGE_COUNT:
            return False, f"Document contains {total_pages} pages, which exceeds the maximum limit of {config.MAX_PAGE_COUNT} pages."
            
        # 5. Extractable Text Check
        total_extracted_text = ""
        for page in reader.pages[:5]:
            text = page.extract_text() or ""
            total_extracted_text += text.strip()
            
        if len(total_extracted_text) < config.MIN_TEXT_CHARS:
            return False, "PDF contains no extractable text. It may be an image-only scanned document without OCR."
            
        return True, "PDF audit passed successfully."

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
