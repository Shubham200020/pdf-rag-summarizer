# 🗺️ Master Roadmap & Feature Specification

## Product Vision
An end-to-end intelligent document platform that ingests PDF files of any length, builds a vector database index, extracts an executive summary and structured learning roadmap, and provides a conversational RAG interface with page citations.

## Implementation Phases

### Phase 1: Streamlit Prototype (Completed)
- [x] Initial Streamlit Python proof-of-concept.
- [x] PyPDFLoader integration and text chunking.
- [x] ChromaDB embedding and local vector store.
- [x] Map-Reduce summary & roadmap chain.
- [x] Streamlit Chat UI with basic citations.

### Phase 2: Decoupled FastAPI Backend & React Frontend (Current Phase)
- [x] Refactor architecture into separate `backend/` (FastAPI) and `frontend/` (React).
- [x] Pydantic v2 schemas for strict API contract validation.
- [x] Async REST endpoints for file upload, roadmap extraction, and RAG search.
- [x] CORS middleware for frontend-backend communication.
- [x] Modern React UI with Tailwind / sleek CSS styling, tabbed interface, upload drag-and-drop, and citation expanders.

### Phase 3: Advanced RAG Features (Future Roadmap)
- [ ] Multi-PDF support (workspace multi-document search).
- [ ] Hybrid Search (BM25 Keyword + Vector Embeddings via Reciprocal Rank Fusion).
- [ ] Document OCR fallback (`pytesseract` for scanned image PDFs).
- [ ] RAG evaluation using `Ragas` framework (faithfulness & answer relevance scores).
- [ ] Export summary/roadmap to Markdown or PDF.
