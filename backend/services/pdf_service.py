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
    """PDF parsing, human-centric semantic chunking, multimodal image extraction, and audit validation service."""
    
    @staticmethod
    def audit_pdf(pdf_path: str, file_size: int) -> Tuple[bool, str]:
        """Audits PDF file against size, encryption, page count, and text/image extractability constraints."""
        # 1. File Size Audit
        if file_size == 0:
            return False, "Uploaded PDF file is empty (0 bytes)."
            
        if file_size > config.MAX_FILE_SIZE_BYTES:
            size_mb = round(file_size / (1024 * 1024), 2)
            return False, f"PDF file size ({size_mb} MB) exceeds maximum allowed limit of {config.MAX_FILE_SIZE_MB} MB."
            
        # 2. Open PDF and check structure
        try:
            reader = PdfReader(pdf_path)
            doc_fitz = fitz.open(pdf_path)
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
            
        # 5. Extractable Text & Embedded Image Audit
        total_extracted_text = ""
        total_images = 0
        for i, page in enumerate(reader.pages[:5]):
            text = page.extract_text() or ""
            total_extracted_text += text.strip()
            if i < len(doc_fitz):
                total_images += len(doc_fitz[i].get_images())

        # Pass audit if either text >= MIN_TEXT_CHARS OR embedded images are present
        if len(total_extracted_text) < config.MIN_TEXT_CHARS and total_images == 0:
            return False, "PDF contains no extractable text or embedded images/scans."
            
        return True, "PDF audit passed successfully."

    @staticmethod
    def process_pdf(pdf_path: str, api_key: str = None) -> Tuple[List[Document], int]:
        """Parses PDF text using Human-Centric Semantic Chunking and extracts embedded images/figures for vector indexing."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")
            
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        total_pages = len(pages)
        
        file_name = os.path.basename(pdf_path)
        
        # Track document headings for topic-aware section metadata
        current_section = "General Overview"
        section_headers = ["TECHNICAL SKILLS", "PROJECTS", "EXPERIENCE", "EDUCATION", "CAREER OBJECTIVE", "CERTIFICATIONS", "SUMMARY", "PUBLICATIONS"]
        
        for p in pages:
            p.metadata["source_file"] = file_name
            p.metadata["content_type"] = "text_chunk"
            if "page" in p.metadata:
                p.metadata["page_label"] = p.metadata["page"] + 1
            
            # Detect active section heading in page content
            for header in section_headers:
                if header in p.page_content.upper():
                    current_section = header
                    break
            p.metadata["section_heading"] = current_section

        # 🧠 Human-Centric Semantic Splitter: Splits cleanly on logical sections, list items, and full sentences
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=[
                "\n\n# ", "\n\n## ", "\n\n### ", 
                "\n\nPROJECTS", "\n\nTECHNICAL SKILLS", "\n\nEXPERIENCE", "\n\nEDUCATION", "\n\nCAREER OBJECTIVE",
                "\n\n\n", "\n\n", 
                "\n• ", "\n- ", "\n* ", "\n1. ", "\n2. ", "\n3. ",
                ". ", "? ", "! ",
                "\n", " "
            ]
        )
        
        text_chunks = splitter.split_documents(pages)
        
        # Clean up each chunk to ensure human readability
        for chunk in text_chunks:
            chunk.page_content = re.sub(r' +', ' ', chunk.page_content).strip()
        
        # 🖼️ Extract and Caption Embedded Images / Diagrams
        image_chunks = ImageService.extract_and_caption_images(pdf_path, api_key=api_key)
        
        all_chunks = text_chunks + image_chunks
        return all_chunks, total_pages
