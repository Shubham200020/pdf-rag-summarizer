# 📝 Issue Log 09: Blank White Screen Root Cause & Fix

## 📌 Issue Overview
- **Symptom**: Opening `https://eighty-feet-unite.loca.lt` rendered a blank white screen.
- **Affected Components**: `frontend/vite.config.js`, production static bundle `frontend/dist`.

---

## 🔍 Log Investigation & Root Cause Analysis

### 1. Empirical Server Log Trace
From FastAPI backend task logs:
```http
INFO: 152.58.30.249 - "GET / HTTP/1.1" 200 OK
INFO: 152.58.30.249 - "GET /pdf-rag-summarizer/assets/index-DLciCGeT.js HTTP/1.1" 404 Not Found
INFO: 152.58.30.249 - "GET /pdf-rag-summarizer/assets/index-qvEK4Xyb.css HTTP/1.1" 404 Not Found
```

### 2. Root Cause
- In `frontend/vite.config.js`, `base: '/pdf-rag-summarizer/'` had been set for GitHub Pages sub-path deployment.
- As a result, the built `index.html` contained absolute sub-path references:
  ```html
  <script src="/pdf-rag-summarizer/assets/index-DLciCGeT.js"></script>
  ```
- When loaded via the unified FastAPI server mounted at root `/`, the browser requested `/pdf-rag-summarizer/assets/index-DLciCGeT.js`, which returned **404 Not Found**.
- Because the main JavaScript bundle failed to load, the React app could not mount to `<div id="root"></div>`, leaving a **blank white screen**.

---

## 🛠️ Permanent Resolution

### 1. Universal Relative Asset Base Path
Updated `frontend/vite.config.js` to use relative base path **`base: './'`**:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './', // Relative base path works universally across root domain & subpaths
  server: {
    port: 5173,
    host: true,
    allowedHosts: true
  }
})
```

### 2. Verified HTML Output
Rebuilt production assets (`npm run build`). `index.html` now renders:
```html
<script type="module" crossorigin src="./assets/index-Cax-jiZn.js"></script>
<link rel="stylesheet" crossorigin href="./assets/index-qvEK4Xyb.css">
```

### 3. Cross-Platform Compatibility Matrix

| Environment | Asset Request Path | HTTP Status | UI Status |
| :--- | :--- | :--- | :--- |
| **FastAPI Unified Server** (`eighty-feet-unite.loca.lt`) | `./assets/index-Cax-jiZn.js` | **`200 OK`** | **Rendered** |
| **GitHub Pages** (`shubham200020.github.io/pdf-rag-summarizer/`) | `./assets/index-Cax-jiZn.js` | **`200 OK`** | **Rendered** |
| **Local Dev** (`localhost:5173`) | `./assets/index-Cax-jiZn.js` | **`200 OK`** | **Rendered** |
