# ☁️ Deployment & Hosting Guide: PDF RAG & Roadmap Summarizer

This document details deployment strategies for hosting the decoupled **FastAPI Backend + React Frontend** application.

---

## Strategy A: Free Tier Deployment (Vercel + Render)

### 1. Frontend Deployment (Vercel / Netlify)
- **Service**: Vercel (Free Tier)
- **Build Settings**:
  - Framework Preset: `Vite`
  - Root Directory: `frontend`
  - Build Command: `npm run build`
  - Output Directory: `dist`
- **Environment Variables**:
  - `VITE_API_BASE_URL=https://your-fastapi-backend.onrender.com/api`

### 2. Backend Deployment (Render.com / Railway)
- **Service**: Render Web Service (Python Runtime)
- **Settings**:
  - Root Directory: `backend`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `OPENAI_API_KEY=your_openai_api_key` (Optional if using free HuggingFace embeddings)

---

## Strategy B: Docker Container Deployment (AWS / DigitalOcean / Render)

### `backend/Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt-get/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend/storage:/app/storage

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

---

## Strategy C: Single VPS Server (Ubuntu + Nginx + Systemd)

1. **Setup Reverse Proxy (`/etc/nginx/sites-available/pdf-rag`)**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # React Static Frontend
    location / {
        root /var/www/pdf-rag/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # FastAPI Backend Proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
2. **Enable SSL**: Run `sudo certbot --nginx -d your-domain.com` for free HTTPS.
