# 📝 Feature Audit & Missing Capabilities Specification

## Overview
This document records the comprehensive feature audit conducted on July 28, 2026. It categorizes currently implemented capabilities, identified missing features, user value assessments, and recommended implementation roadmaps for future work.

---

## 📊 Current vs. Missing Feature Matrix

### ✅ 1. Implemented Features
- **PDF Ingestion & Pre-Embedding Audit**: Validates file size (≤50 MB), encryption/password status, page count (≤200 pages), and text/image extractability before vector indexing. Shows explicit red rejection alerts on failure.
- **Multimodal PDF Image Extraction**: PyMuPDF (`fitz`) extracts embedded diagrams, charts, and figures. OpenAI Vision (`gpt-4o-mini`) generates semantic figure descriptions indexed into ChromaDB.
- **Map-Reduce Executive Summary & Roadmap**: LCEL chain (`prompt | llm | StrOutputParser()`) generates structured learning milestones.
- **RAG Q&A with Expandable Citations**: Retrieves relevant context with page labels, source filename, and text snippets.
- **Zero-Config Open-Source Fallback**: Local HuggingFace embeddings (`all-MiniLM-L6-v2`) for $0-cost execution without OpenAI API keys.
- **Unified FastAPI + React Deployment**: Mounted production React build directly at `/` inside FastAPI. Universal relative asset path (`base: './'`).

---

## 🚨 2. Audit Gaps & Missing Features (Backlog for Future Work)

### 📌 Feature Gap 1: Roadmap Export (PDF / Markdown / Copy)
- **Status**: Pending Implementation
- **Description**: Add UI export controls on the Summary & Roadmap tab to download generated roadmaps as `.md` files, export formatted `.pdf` documents, or copy text directly to clipboard.
- **Priority**: High (Phase 1)

### 📌 Feature Gap 2: Multi-PDF Document Workspace
- **Status**: Pending Implementation
- **Description**: Enable uploading and indexing multiple PDF files into a unified workspace collection for cross-document RAG retrieval and comparative analysis.
- **Priority**: High (Phase 2)

### 📌 Feature Gap 3: Document OCR Fallback (`pytesseract`)
- **Status**: Pending Implementation
- **Description**: Add Optical Character Recognition (OCR) for scanned image-only PDF documents lacking embedded text or vector figures.
- **Priority**: Medium (Phase 3)

### 📌 Feature Gap 4: Hybrid Search (BM25 + ChromaDB Vector RRF)
- **Status**: Pending Implementation
- **Description**: Combine keyword BM25 retrieval with ChromaDB dense vector search using Reciprocal Rank Fusion (RRF) for enhanced retrieval accuracy on numbers, code snippets, and exact terms.
- **Priority**: Advanced (Phase 4)

---

## 🗺️ Roadmap Execution Checklist

- [ ] **Task 10.1**: Implement Markdown & PDF export buttons on `SummaryRoadmapView.jsx`.
- [ ] **Task 10.2**: Update `pdf_router.py` & `rag_service.py` to support multi-file document workspace IDs.
- [ ] **Task 10.3**: Add `pytesseract` OCR processing pipeline in `pdf_service.py`.
- [ ] **Task 10.4**: Integrate BM25 keyword retriever with ChromaDB vector retriever.
