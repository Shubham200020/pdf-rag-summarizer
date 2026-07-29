# 📝 Localtunnel 503 & Network Error Audit Log

## Incident Overview
- **Symptom**: Frontend on `pdf-rag-summarizer.vercel.app` displaying `Network Error` or `503 Tunnel Unavailable` when attempting to upload PDF files to `https://eighty-feet-unite.loca.lt/api/pdf/upload`.
- **Date Recorded**: July 29, 2026

---

## 🔍 Root Cause Analysis

1. **Localtunnel Socket Disconnects (503 Tunnel Unavailable)**:
   - Free localtunnel public sockets periodically time out or disconnect when idle or after heavy socket traffic, causing `https://eighty-feet-unite.loca.lt` to return HTTP `503 Service Unavailable`.
   - **Fix**: Restarted Uvicorn server on port 8000 and re-bound localtunnel with `npx localtunnel --port 8000 --subdomain eighty-feet-unite`.

2. **Localtunnel Security Reminder Page (Network Error)**:
   - Localtunnel presents an HTML landing page ("Click to Continue" / IP verification prompt) to new client IP addresses.
   - When web applications (like Vercel frontend) issue cross-origin `POST` or `OPTIONS` preflight requests to localtunnel without authorization, localtunnel returns HTML instead of JSON headers, causing browsers to block CORS with `Network Error` or `405 Method Not Allowed`.
   - **Fix**:
     - Added `'bypass-tunnel-reminder': 'true'` request header to `apiClient` in `frontend/src/api/client.js`.
     - Added a 1-click authorization helper banner in `frontend/src/components/PdfUploader.jsx` providing the direct link to authorize IP (`45.250.227.158`).

---

## 🛡️ Permanent Resolution & Backup Recommendations
- **For Local Machine Tunneling**: Re-run `npx localtunnel --port 8000 --subdomain eighty-feet-unite` whenever local machine restarts.
- **For 24/7 Laptop-Independent Hosting**: Deploy Docker container to **Render Blueprint** (`render.yaml`), **Railway** (`railway.json`), or **Hugging Face Spaces** (`Dockerfile`).
