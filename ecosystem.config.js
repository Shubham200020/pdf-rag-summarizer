module.exports = {
  apps: [
    {
      name: "pdf-backend",
      script: "D:/Program/Projects/pdf-rag-summarizer/backend/venv/Scripts/python.exe",
      args: "-m uvicorn main:app --host 0.0.0.0 --port 8000",
      cwd: "D:/Program/Projects/pdf-rag-summarizer/backend",
      autorestart: true,
      max_restarts: 50,
      restart_delay: 2000,
      env: {
        PYTHONIOENCODING: "utf-8"
      }
    },
    {
      name: "pdf-tunnel",
      script: "npx",
      args: "localtunnel --port 8000 --subdomain eighty-feet-unite",
      cwd: "D:/Program/Projects/pdf-rag-summarizer",
      autorestart: true,
      max_restarts: 100,
      restart_delay: 3000
    }
  ]
};
