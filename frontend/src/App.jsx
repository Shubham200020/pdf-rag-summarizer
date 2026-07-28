import React, { useState, useEffect } from 'react';
import PdfUploader from './components/PdfUploader';
import SummaryRoadmapView from './components/SummaryRoadmapView';
import RagChat from './components/RagChat';
import { FileText, MessageSquare, Key, Server, Sparkles, Layers, CheckCircle2, AlertCircle } from 'lucide-react';
import { getApiBaseUrl } from './api/client';
import axios from 'axios';

export default function App() {
  const [apiKey, setApiKey] = useState(localStorage.getItem('openai_api_key') || '');
  const [backendUrl, setBackendUrl] = useState(localStorage.getItem('custom_backend_url') || 'https://eighty-feet-unite.loca.lt');
  const [backendStatus, setBackendStatus] = useState('checking'); // 'connected', 'disconnected', 'checking'
  const [activeDocument, setActiveDocument] = useState(null);
  const [activeTab, setActiveTab] = useState('summary');

  useEffect(() => {
    localStorage.setItem('openai_api_key', apiKey);
  }, [apiKey]);

  // Check backend server health
  const checkBackendHealth = async (url) => {
    setBackendStatus('checking');
    try {
      const cleanUrl = url.endsWith('/api') ? url : `${url.replace(/\/$/, '')}/api`;
      await axios.get(`${cleanUrl}/health`, { timeout: 4000 });
      setBackendStatus('connected');
    } catch (err) {
      setBackendStatus('disconnected');
    }
  };

  useEffect(() => {
    checkBackendHealth(backendUrl);
  }, [backendUrl]);

  const handleBackendUrlChange = (e) => {
    const val = e.target.value;
    setBackendUrl(val);
    if (val) {
      localStorage.setItem('custom_backend_url', val);
    } else {
      localStorage.removeItem('custom_backend_url');
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="brand-badge">
          <Layers size={14} /> Intelligent Document Platform
        </div>
        <h1>PDF RAG & Roadmap Engine</h1>
        <p>Extract structured roadmaps, index visual diagrams, and query PDF documents with page citations.</p>

        {/* Configurations */}
        <div className="config-bar">
          <div className="input-container">
            <Key size={16} style={{ color: '#9ca3af', marginRight: '0.75rem' }} />
            <input 
              type="password"
              placeholder="OpenAI API Key (Optional - leave empty for zero-config local embeddings)"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
          </div>

          <div className="input-container" style={{ position: 'relative' }}>
            <Server size={16} style={{ color: '#6366f1', marginRight: '0.75rem' }} />
            <input 
              type="text"
              placeholder="Backend Server URL (e.g. https://eighty-feet-unite.loca.lt)"
              value={backendUrl}
              onChange={handleBackendUrlChange}
            />
            <span style={{ position: 'absolute', right: '12px', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
              {backendStatus === 'connected' ? (
                <span style={{ color: '#10b981', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                  <CheckCircle2 size={14} /> Connected
                </span>
              ) : backendStatus === 'disconnected' ? (
                <span style={{ color: '#ef4444', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                  <AlertCircle size={14} /> Disconnected
                </span>
              ) : (
                <span style={{ color: '#9ca3af' }}>Connecting...</span>
              )}
            </span>
          </div>
        </div>
      </header>

      <main>
        <PdfUploader apiKey={apiKey} onPdfUploaded={(doc) => setActiveDocument(doc)} />

        {activeDocument ? (
          <div style={{ marginTop: '2rem' }}>
            <div className="tabs-header">
              <button 
                className={`tab-btn ${activeTab === 'summary' ? 'active' : ''}`}
                onClick={() => setActiveTab('summary')}
              >
                <Sparkles size={16} /> Summary & Roadmap
              </button>
              <button 
                className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
                onClick={() => setActiveTab('chat')}
              >
                <MessageSquare size={16} /> Conversational RAG Q&A
              </button>
            </div>

            {activeTab === 'summary' ? (
              <SummaryRoadmapView documentId={activeDocument.document_id} apiKey={apiKey} />
            ) : (
              <RagChat documentId={activeDocument.document_id} apiKey={apiKey} />
            )}
          </div>
        ) : (
          <div style={{ textAlign: 'center', marginTop: '2.5rem', color: '#6b7280', fontSize: '0.9rem' }}>
            <p>Upload a PDF document above to get started.</p>
          </div>
        )}
      </main>
    </div>
  );
}
