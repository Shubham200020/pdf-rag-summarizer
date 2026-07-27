import sys
import os

# Ensure standard output and error streams use UTF-8 encoding on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import pdf_router, chat_router

app = FastAPI(
    title="PDF RAG & Roadmap Summarizer API",
    description="FastAPI backend supporting PDF parsing, chunking, roadmap summarization, and RAG retrieval.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_router.router)
app.include_router(chat_router.router)

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "app": "PDF RAG & Roadmap Summarizer API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
