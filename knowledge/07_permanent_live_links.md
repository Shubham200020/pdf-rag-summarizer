# 🌐 Permanent Live Access Links & Memory Record

## Primary Public Web Application
- **Static Live Link**: `https://eighty-feet-unite.loca.lt`
- **Fallback Live Link**: `https://cold-lizard-82.loca.lt`
- **Tunnel Password / IP Verification**: `45.250.227.158`
- **GitHub Repository**: `https://github.com/Shubham200020/pdf-rag-summarizer`
- **GitHub Pages Link**: `https://shubham200020.github.io/pdf-rag-summarizer/`

---

## 📌 Subdomain Lock Rule
When starting localtunnel, ALWAYS specify the fixed subdomain flag so that the public URL never changes across restarts or deployments:

```powershell
npx localtunnel --port 8000 --subdomain eighty-feet-unite
```

---

## 🐛 Fixed Bugs Record
1. **`os.path.getsize` syntax error fixed in `pdf_router.py`**:
   - Replaced invalid `os.path.path.getsize` call with `os.path.getsize(temp_path)` to prevent `ntpath` AttributeError on Windows & mobile requests.
2. **Mobile Relative API Routes**:
   - `client.js` uses relative `/api` paths so mobile devices route automatically to the host server.
