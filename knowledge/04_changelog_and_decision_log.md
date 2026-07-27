# 📝 Change & Decision Log (Memory Storage)

## Log Entry: 2026-07-27
### Changes & Architecture Evolution
1. **Repository Restructuring**: Created dedicated `knowledge/` memory directory storing full architecture docs, master roadmap, API contracts, and decision history.
2. **FastAPI Backend Infrastructure**:
   - Built a modular FastAPI backend in `backend/`.
   - Separated services: `pdf_service.py`, `vector_service.py`, `summarizer_service.py`, `rag_service.py`.
   - Implemented CORS middleware supporting React frontend integration (`http://localhost:5173`).
   - Standardized Pydantic schemas for request/response payloads.
3. **React Frontend (Vite UI)**:
   - Built a modern, tabbed single-page application using React & CSS.
   - Components created:
     - `PdfUploader`: Drag & drop upload with loading progress.
     - `SummaryRoadmapView`: Formatted markdown rendering for summary & action roadmap.
     - `RagChat`: Real-time Q&A interface with interactive source citation expanders.
