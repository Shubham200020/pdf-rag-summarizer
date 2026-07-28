# 🌐 Comprehensive 24/7 Cloud Hosting Platforms Guide

## Overview
This guide documents top 24/7 cloud hosting platforms to deploy the PDF RAG & Roadmap Summarizer application so it runs 24/7/365 without requiring a local laptop to be turned on.

---

## 🏆 Top 24/7 Cloud Hosting Platforms

### 1. Hugging Face Spaces (100% Free Docker Cloud) — **Top Recommendation**
- **Free Tier**: 16 GB RAM, 2 vCPU, 50 GB storage (100% Free 24/7).
- **Container**: Native Docker container support via root `Dockerfile`.
- **Laptop Needed?**: No (Hosted 24/7 in Google Cloud / AWS).
- **Deploy Link**: [huggingface.co/new-space](https://huggingface.co/new-space)
- **Setup**: Select **Docker SDK** ➔ Import `Shubham200020/pdf-rag-summarizer`.

---

### 2. Render.com (100% Free Web Service)
- **Free Tier**: 512 MB RAM, free SSL certificates, GitHub auto-deploys.
- **Blueprint**: Auto-configured via [`render.yaml`](file:///D:/Program/Projects/pdf-rag-summarizer/render.yaml).
- **Laptop Needed?**: No (Hosted 24/7 on Render cloud).
- **Deploy Link**: [dashboard.render.com/select-repo?type=blueprint](https://dashboard.render.com/select-repo?type=blueprint)

---

### 3. Railway.app (Fast Cloud Infrastructure)
- **Free Tier**: $5 free monthly credit (~500 hours runtime).
- **Config**: Auto-configured via [`railway.json`](file:///D:/Program/Projects/pdf-rag-summarizer/railway.json).
- **Laptop Needed?**: No.
- **Deploy Link**: [railway.app/new](https://railway.app/new)

---

### 4. Koyeb (Serverless Docker Cloud)
- **Free Tier**: 1 Free Nano instance (512 MB RAM, 24/7 runtime).
- **Container**: Automatic Dockerfile build from GitHub.
- **Laptop Needed?**: No.
- **Deploy Link**: [app.koyeb.com](https://app.koyeb.com)

---

### 5. Fly.io (Micro-VM Global Containers)
- **Free Tier**: Free micro-VM allowance.
- **Container**: Firecracker Docker container runner.
- **Laptop Needed?**: No.
- **Deploy**: Run `fly launch` in project directory.

---

### 6. Decoupled Vercel (Frontend) + Cloud Backend
- **Frontend**: [vercel.com/new](https://vercel.com/new) (100% Free high-speed global CDN for React).
- **Backend**: Render / Railway / Hugging Face for FastAPI Python backend.
