import os
import re
import fitz
from typing import List, Tuple
from pypdf import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from services.image_service import ImageService
import config

class PDFService:
    """PDF parsing, human-centric semantic chunking, section metadata tagging, and audit validation service."""
    
    @staticmethod
    def audit_pdf(pdf_path: str, file_size: int) -> Tuple[bool, str]:
        """Audits PDF file against size, encryption, page count, and text/image extractability constraints."""
        if file_size == 0:
            return False, "Uploaded PDF file is empty (0 bytes)."
            
        if file_size > config.MAX_FILE_SIZE_BYTES:
            size_mb = round(file_size / (1024 * 1024), 2)
            return False, f"PDF file size ({size_mb} MB) exceeds maximum allowed limit of {config.MAX_FILE_SIZE_MB} MB."
            
        try:
            reader = PdfReader(pdf_path)
            doc_fitz = fitz.open(pdf_path)
        except Exception as e:
            return False, f"Corrupted or invalid PDF structure: {str(e)}"
            
        if reader.is_encrypted:
            return False, "PDF is password-protected or encrypted. Please remove password protection before uploading."
            
        total_pages = len(reader.pages)
        if total_pages == 0:
            return False, "PDF contains 0 pages."
            
        if total_pages > config.MAX_PAGE_COUNT:
            return False, f"Document contains {total_pages} pages, which exceeds maximum limit of {config.MAX_PAGE_COUNT} pages."
            
        total_extracted_text = ""
        total_images = 0
        for i, page in enumerate(reader.pages[:5]):
            text = page.extract_text() or ""
            total_extracted_text += text.strip()
            if i < len(doc_fitz):
                total_images += len(doc_fitz[i].get_images())

        if len(total_extracted_text) < config.MIN_TEXT_CHARS and total_images == 0:
            return False, "PDF contains no extractable text or embedded images/scans."
            
        return True, "PDF audit passed successfully."

    @staticmethod
    def process_pdf(pdf_path: str, api_key: str = None) -> Tuple[List[Document], int]:
        """Parses PDF text using Section-Preserving Semantic Chunking and extracts embedded images/figures for vector indexing."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")
            
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        total_pages = len(pages)
        file_name = os.path.basename(pdf_path)
        
        section_headers = ["TECHNICAL SKILLS", "ACADEMIC PROJECTS", "PROJECTS", "EXPERIENCE", "EDUCATION", "TRAINING", "CAREER OBJECTIVE", "CERTIFICATIONS"]
        
        for p in pages:
            p.metadata["source_file"] = file_name
            p.metadata["content_type"] = "text_chunk"
            if "page" in p.metadata:
                p.metadata["page_label"] = p.metadata["page"] + 1

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=[
                "\n\nTECHNICAL SKILLS", "\n\nACADEMIC PROJECTS", "\n\nPROJECTS", "\n\nEXPERIENCE", "\n\nEDUCATION", "\n\nTRAINING",
                "\n\n# ", "\n\n## ", "\n\n### ",
                "\n\n\n", "\n\n", 
                "\n• ", "\n- ", "\n* ", "\n➢ ", "\n1. ", "\n2. ", "\n3. ",
                ". ", "? ", "! ",
                "\n", " "
            ]
        )
        
        text_chunks = splitter.split_documents(pages)
        
        # Tag active section heading on each individual chunk
        for chunk in text_chunks:
            chunk.page_content = re.sub(r' +', ' ', chunk.page_content).strip()
            active_sec = "GENERAL"
            content_upper = chunk.page_content.upper()
            for header in section_headers:
                if header in content_upper:
                    active_sec = header
                    break
            chunk.metadata["section_heading"] = active_sec
        
        # Extract and Caption Embedded Images / Diagrams
        image_chunks = ImageService.extract_and_caption_images(pdf_path, api_key=api_key)
        
        all_chunks = text_chunks + image_chunks
        return all_chunks, total_pages
