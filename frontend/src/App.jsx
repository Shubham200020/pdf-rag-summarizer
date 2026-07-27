import React, { useState } from 'react';
import PdfUploader from './components/PdfUploader';
import SummaryRoadmapView from './components/SummaryRoadmapView';
import RagChat from './components/RagChat';
import { Key } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('summary');
  const [uploadedPdf, setUploadedPdf] = useState(null);
  const [apiKey, setApiKey] = useState('');

  return (
    <div className="app-container">
      <header className="header">
        <h1>📚 PDF RAG & Roadmap Summarizer</h1>
        <p>Decoupled FastAPI + React AI Application with LangChain & Vector Retrieval</p>
        
        {/* OpenAI API Key Setting */}
        <div style={{ maxWidth: '500px', margin: '1.5rem auto 0', display: 'flex', alignItems: 'center', gap: '0.5rem', background: '#1e293b', padding: '0.5rem 1rem', borderRadius: '8px', border: '1px solid #334155' }}>
          <Key size={18} style={{ color: '#818cf8' }} />
          <input 
            type="password" 
            placeholder="Paste OpenAI API Key here (or set OPENAI_API_KEY in backend/.env)" 
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            style={{ background: 'none', border: 'none', color: '#fff', width: '100%', outline: 'none', fontSize: '0.9rem' }}
          />
        </div>
      </header>

      {/* PDF Upload Section */}
      <PdfUploader apiKey={apiKey} onPdfUploaded={(info) => setUploadedPdf(info)} />

      {/* Tabbed Navigation */}
      {uploadedPdf ? (
        <>
          <div className="tabs-header">
            <button 
              className={`tab-btn ${activeTab === 'summary' ? 'active' : ''}`}
              onClick={() => setActiveTab('summary')}
            >
              📝 Summary & Roadmap
            </button>
            <button 
              className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
              onClick={() => setActiveTab('chat')}
            >
              💬 Conversational RAG Chat
            </button>
          </div>

          {activeTab === 'summary' && (
            <SummaryRoadmapView 
              documentId={uploadedPdf.document_id} 
              apiKey={apiKey} 
            />
          )}

          {activeTab === 'chat' && (
            <RagChat 
              documentId={uploadedPdf.document_id} 
              apiKey={apiKey} 
            />
          )}
        </>
      ) : (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#94a3b8' }}>
          <p>👇 Upload a PDF document above to get started.</p>
        </div>
      )}
    </div>
  );
}
