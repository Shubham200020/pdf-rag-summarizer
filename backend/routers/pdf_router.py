import os
import shutil
import uuid
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from schemas import UploadResponse, SummarizeRequest, SummarizeResponse
from services.pdf_service import PDFService
from services.vector_service import VectorService
from services.summarizer_service import SummarizerService
import config

router = APIRouter(prefix="/api/pdf", tags=["PDF Processing"])

document_cache = {}

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    api_key: Optional[str] = Form(None)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="PDF Cannot Be Embedded: Only PDF files are supported."
        )
        
    doc_id = str(uuid.uuid4())[:8]
    temp_path = os.path.join(config.TEMP_UPLOAD_DIR, f"{doc_id}_{file.filename}")
    
    try:
        # Save temp file to perform audit
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        file_size = os.path.getsize(temp_path)
        
        # 🔍 Run Mandatory Pre-Embedding PDF Audit
        is_valid, audit_reason = PDFService.audit_pdf(temp_path, file_size)
        if not is_valid:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise HTTPException(
                status_code=400,
                detail=f"PDF Cannot Be Embedded: {audit_reason}"
            )
            
        key = api_key or config.OPENAI_API_KEY
        
        # Multimodal Text + Image Caption Processing
        chunks, total_pages = PDFService.process_pdf(temp_path, api_key=key)
        VectorService.create_collection(chunks, collection_name=doc_id, api_key=key)
        
        document_cache[doc_id] = {
            "filename": file.filename,
            "temp_path": temp_path,
            "chunks": chunks,
            "total_pages": total_pages
        }
        
        return UploadResponse(
            filename=file.filename,
            document_id=doc_id,
            total_pages=total_pages,
            total_chunks=len(chunks),
            message="Multimodal PDF audit passed, images extracted, and vector embedding completed successfully."
        )
    except HTTPException:
        raise
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"PDF Cannot Be Embedded: {str(e)}")

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_pdf(req: SummarizeRequest):
    doc_data = document_cache.get(req.document_id)
    if not doc_data:
        raise HTTPException(status_code=404, detail="Document ID not found. Please upload the PDF first.")
        
    key = req.api_key or config.OPENAI_API_KEY
    try:
        summary_text = SummarizerService.generate_summary(
            chunks=doc_data["chunks"],
            api_key=key,
            model_name=req.model_name
        )
        return SummarizeResponse(
            filename=doc_data["filename"],
            summary_and_roadmap=summary_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to summarize document: {str(e)}")
