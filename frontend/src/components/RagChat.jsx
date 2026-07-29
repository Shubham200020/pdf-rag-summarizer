import React, { useState, useRef, useEffect } from 'react';
import { queryChatApi } from '../api/client';
import { Send, Bot, User, BookOpen, Loader } from 'lucide-react';

export default function RagChat({ documentId, apiKey }) {
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const chatBottomRef = useRef(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputQuery.trim() || !documentId) return;

    const userMessage = inputQuery;
    setInputQuery('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const data = await queryChatApi(documentId, userMessage, apiKey);
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

  // Helper function to format answer text nicely with paragraphs
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
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
        <Bot size={28} style={{ color: '#6366f1' }} />
        <div>
          <h2 style={{ fontSize: '1.25rem', color: '#f9fafb', fontWeight: 700 }}>Conversational RAG Q&A</h2>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Ask questions about your PDF and receive grounded answers with page citations.</p>
        </div>
      </div>

      <div className="chat-box">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: '#94a3b8', padding: '3.5rem 1rem' }}>
            <Bot size={44} style={{ margin: '0 auto 1rem', color: '#6366f1', opacity: 0.8 }} />
            <h4 style={{ color: '#f8fafc', fontSize: '1.05rem', fontWeight: 600, marginBottom: '0.35rem' }}>Ask anything about your document</h4>
            <p style={{ fontSize: '0.875rem' }}>Type a question below to perform semantic vector search across pages.</p>
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
                  <BookOpen size={14} /> Grounded Page Citations:
                </span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                  {msg.sources.map((src, i) => (
                    <div key={i} className="citation-badge">
                      <strong style={{ color: '#6ee7b7' }}>Page {src.page}:</strong> <em>"{src.snippet}"</em>
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
            <span>Searching vector context and generating citation answer...</span>
          </div>
        )}
        <div ref={chatBottomRef} />
      </div>

      <form onSubmit={handleSend} style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
        <input 
          className="input-field" 
          type="text"
          placeholder={documentId ? "Type your question about the PDF..." : "Please upload a PDF document first..."}
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
