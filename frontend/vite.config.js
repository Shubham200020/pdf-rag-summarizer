import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Use relative base './' so assets load seamlessly on both unified FastAPI (root '/') and GitHub Pages ('/pdf-rag-summarizer/')
export default defineConfig({
  plugins: [react()],
  base: './',
  server: {
    port: 5173,
    host: true,
    allowedHosts: true
  }
})
