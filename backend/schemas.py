from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class UploadResponse(BaseModel):
    filename: str
    document_id: str
    total_pages: int
    total_chunks: int
    message: str

class SummarizeRequest(BaseModel):
    document_id: str = Field(..., description="Document collection ID")
    model_name: Optional[str] = "gpt-4o-mini"
    api_key: Optional[str] = None

class SummarizeResponse(BaseModel):
    filename: str
    summary_and_roadmap: str

class ChatQueryRequest(BaseModel):
    document_id: str = Field(..., description="Document collection ID")
    question: str = Field(..., description="User query")
    model_name: Optional[str] = "gpt-4o-mini"
    api_key: Optional[str] = None

class SourceCitation(BaseModel):
    page: Any
    file: str
    snippet: str

class ChatQueryResponse(BaseModel):
    answer: str
    sources: List[SourceCitation]
