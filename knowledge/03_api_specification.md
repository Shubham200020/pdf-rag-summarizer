# 📡 REST API Specification (FastAPI Backend)

Base URL: `http://localhost:8000`

---

## Endpoints

### 1. Health Check
`GET /`
- **Response**: `{"status": "ok", "message": "PDF RAG & Summarizer API Running"}`

---

### 2. Upload and Index PDF
`POST /api/pdf/upload`
- **Content-Type**: `multipart/form-data`
- **Request Body**:
  - `file`: PDF file blob
- **Response**:
```json
{
  "filename": "sample.pdf",
  "document_id": "user_pdf",
  "total_pages": 12,
  "total_chunks": 35,
  "message": "PDF uploaded and indexed successfully."
}
```

---

### 3. Generate Summary & Roadmap
`POST /api/pdf/summarize`
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
  "document_id": "user_pdf",
  "model_name": "gpt-4o-mini",
  "api_key": "optional_override_key"
}
```
- **Response**:
```json
{
  "filename": "sample.pdf",
  "summary_and_roadmap": "### 📌 EXECUTIVE SUMMARY\n..."
}
```

---

### 4. Query RAG Chat Engine
`POST /api/chat/query`
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
  "document_id": "user_pdf",
  "question": "What is the core topic of chapter 3?",
  "model_name": "gpt-4o-mini",
  "api_key": "optional_override_key"
}
```
- **Response**:
```json
{
  "answer": "Chapter 3 focuses on...",
  "sources": [
    {
      "page": 5,
      "file": "sample.pdf",
      "snippet": "Chapter 3 introduces the concepts of vector indexing..."
    }
  ]
}
```
