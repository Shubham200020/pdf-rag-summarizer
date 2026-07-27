import React, { useState } from 'react';
import { queryChatApi } from '../api/client';
import { Send, Bot, User, BookOpen, Loader } from 'lucide-react';

export default function RagChat({ documentId, apiKey }) {
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);

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

  return (
    <div className="card">
      <h2 style={{ marginBottom: '1rem' }}>💬 Conversational RAG Chat</h2>
      <p style={{ color: '#94a3b8', marginBottom: '1.5rem' }}>Ask questions about your PDF and receive grounded answers with page citations.</p>

      <div className="chat-box">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: '#94a3b8', padding: '3rem 0' }}>
            <Bot size={48} style={{ margin: '0 auto 1rem', color: '#6366f1' }} />
            <p>Ask any question about your uploaded document!</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <div style={{ fontWeight: 600, marginBottom: '0.25rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              {msg.role === 'user' ? <User size={14} /> : <Bot size={14} />}
              {msg.role === 'user' ? 'You' : 'PDF Assistant'}
            </div>
            <div>{msg.content}</div>

            {msg.sources && msg.sources.length > 0 && (
              <div style={{ marginTop: '0.75rem', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '0.5rem' }}>
                <span style={{ fontSize: '0.8rem', color: '#34d399', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                  <BookOpen size={12} /> Page Citations:
                </span>
                {msg.sources.map((src, i) => (
                  <div key={i} className="citation-badge" style={{ display: 'block', margin: '0.25rem 0' }}>
                    <strong>Page {src.page}</strong>: <em>"{src.snippet}"</em>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="chat-message assistant" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Loader className="animate-spin" size={16} /> Searching document context...
          </div>
        )}
      </div>

      <form onSubmit={handleSend} style={{ display: 'flex', gap: '0.75rem' }}>
        <input 
          className="input-field" 
          type="text"
          placeholder={documentId ? "Ask anything about your PDF..." : "Please upload a PDF first..."}
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
