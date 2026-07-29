from fastapi import APIRouter, HTTPException
from schemas import ChatQueryRequest, ChatQueryResponse
from services.rag_service import RAGService

router = APIRouter(prefix="/api/chat", tags=["RAG Chat"])

@router.post("/query", response_model=ChatQueryResponse)
async def query_chat(req: ChatQueryRequest):
    try:
        res = RAGService.query(
            document_id=req.document_id,
            document_ids=req.document_ids,
            question=req.question,
            api_key=req.api_key,
            model_name=req.model_name,
            enable_web_search=req.enable_web_search or False,
            chat_history=req.chat_history
        )
        return ChatQueryResponse(
            answer=res["answer"],
            sources=res["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Retrieval failed: {str(e)}")
