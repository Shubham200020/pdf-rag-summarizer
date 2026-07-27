# 📌 Pending Work & Fix Reminder Log

## Overview
This document records the user's explicit instruction to set a reminder for pending issues and future maintenance tasks.

---

## 📋 Reminders & Next Steps (To Fix Later)

1. **GitHub Pages API Routing / Cloud Backend Deployment**:
   - The static GitHub Pages frontend (`https://shubham200020.github.io/pdf-rag-summarizer/`) requires an active 24/7 backend API endpoint.
   - *Future Fix*: Deploy `backend/` to Render.com / Railway so GitHub Pages automatically connects to a permanent cloud backend without requiring local tunnel sessions.

2. **Localtunnel Session Re-establishment**:
   - Free localtunnel connections periodically drop when local terminal background tasks reset.
   - *Future Fix*: Run a persistent background supervisor daemon or Docker container (`docker-compose up`).

3. **Missing Features Implementation Backlog** (From `knowledge/10_feature_audit_and_missing_capabilities.md`):
   - [ ] **Task 1**: Implement Summary & Roadmap export (PDF / Markdown / Copy to Clipboard).
   - [ ] **Task 2**: Implement Multi-PDF Document Workspace (cross-document RAG search).
   - [ ] **Task 3**: Add system OCR fallback for scanned PDF documents.
   - [ ] **Task 4**: Integrate Hybrid Search (BM25 Keyword + Vector RRF).

---

## 📌 How to Resume
When you are ready to resume work, simply say:
> *"Let's review the pending reminders and fix the issue."*
