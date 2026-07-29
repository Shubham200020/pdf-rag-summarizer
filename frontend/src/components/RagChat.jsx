import React, { useState, useRef, useEffect } from 'react';
import { queryChatApi } from '../api/client';
import { Send, Bot, User, BookOpen, Loader, Globe } from 'lucide-react';

export default function RagChat({ documentId, apiKey }) {
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [enableWebSearch, setEnableWebSearch] = useState(false);
  const chatBottomRef = useRef(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputQuery.trim() || !documentId) return;

    const userMessage = inputQuery;
    setInputQuery('');
    
    // Format past chat history for backend
    const chatHistory = messages.map(m => ({
      role: m.role,
      content: m.content
    }));

    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const data = await queryChatApi(documentId, userMessage, apiKey, 'gpt-4o-mini', enableWebSearch, chatHistory);
      setMessages(prev => [
        ...prev, 
        { role: 'assistant', content: data.answer, sources: data.sources }
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev, 
        { role: 'assistant', content: 'Sorry, I encountered an error searching your document.', sources: [] }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const renderFormattedText = (text) => {
    if (!text) return null;
    return text.split('\n').map((paragraph, i) => {
      if (!paragraph.trim()) return <div key={i} style={{ height: '0.5rem' }} />;
      return (
        <p key={i} style={{ marginBottom: '0.5rem', lineHeight: '1.65' }}>
          {paragraph}
        </p>
      );
    });
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <Bot size={28} style={{ color: '#6366f1' }} />
          <div>
            <h2 style={{ fontSize: '1.25rem', color: '#f9fafb', fontWeight: 700 }}>Conversational RAG Q&A</h2>
            <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Ask questions about your PDF and receive grounded answers with page citations.</p>
          </div>
        </div>

        <label 
          style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '0.5rem', 
            background: enableWebSearch ? 'rgba(99, 102, 241, 0.18)' : 'rgba(31, 41, 55, 0.6)', 
            border: `1px solid ${enableWebSearch ? '#6366f1' : '#374151'}`,
            padding: '0.45rem 0.85rem',
            borderRadius: '9999px',
            cursor: 'pointer',
            fontSize: '0.825rem',
            color: enableWebSearch ? '#a5b4fc' : '#9ca3af',
            userSelect: 'none',
            transition: 'all 0.2s ease'
          }}
        >
          <Globe size={15} style={{ color: enableWebSearch ? '#818cf8' : '#9ca3af' }} />
          <span style={{ fontWeight: 600 }}>Real-World Web Data</span>
          <input 
            type="checkbox"
            checked={enableWebSearch}
            onChange={(e) => setEnableWebSearch(e.target.checked)}
            style={{ cursor: 'pointer', accentColor: '#6366f1' }}
          />
        </label>
      </div>

      <div className="chat-box">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: '#94a3b8', padding: '3.5rem 1rem' }}>
            <Bot size={44} style={{ margin: '0 auto 1rem', color: '#6366f1', opacity: 0.8 }} />
            <h4 style={{ color: '#f8fafc', fontSize: '1.05rem', fontWeight: 600, marginBottom: '0.35rem' }}>Ask anything about your document</h4>
            <p style={{ fontSize: '0.875rem' }}>Type a question below to perform hybrid vector and keyword search across pages.</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <div style={{ fontWeight: 700, marginBottom: '0.5rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem', color: msg.role === 'user' ? '#818cf8' : '#34d399' }}>
              {msg.role === 'user' ? <User size={15} /> : <Bot size={15} />}
              {msg.role === 'user' ? 'You' : 'PDF Assistant'}
            </div>

            <div style={{ color: '#f8fafc', fontSize: '0.95rem' }}>
              {renderFormattedText(msg.content)}
            </div>

            {msg.sources && msg.sources.length > 0 && (
              <div style={{ marginTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '0.75rem' }}>
                <span style={{ fontSize: '0.825rem', color: '#34d399', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.35rem', marginBottom: '0.5rem' }}>
                  <BookOpen size={14} /> Grounded Page & Web Citations:
                </span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                  {msg.sources.map((src, i) => (
                    <div key={i} className="citation-badge">
                      <strong style={{ color: '#6ee7b7' }}>{src.page}:</strong> <em>"{src.snippet}"</em>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="chat-message assistant" style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#94a3b8' }}>
            <Loader className="animate-spin" size={18} style={{ color: '#6366f1' }} />
            <span>Performing Hybrid BM25 & Vector Search...</span>
          </div>
        )}
        <div ref={chatBottomRef} />
      </div>

      <form onSubmit={handleSend} style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
        <input 
          className="input-field" 
          type="text"
          placeholder={documentId ? (enableWebSearch ? "Ask PDF question + search live real-world web data..." : "Type your question about the PDF...") : "Please upload a PDF document first..."}
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          disabled={!documentId || loading}
        />
        <button type="submit" className="btn" disabled={!documentId || loading || !inputQuery.trim()}>
          <Send size={18} /> Send
        </button>
      </form>
    </div>
  );
}
