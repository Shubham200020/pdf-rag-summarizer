import React, { useState } from 'react';
import { summarizePdfApi } from '../api/client';
import ReactMarkdown from 'react-markdown';
import { Sparkles, Loader, FileCheck } from 'lucide-react';

export default function SummaryRoadmapView({ documentId, apiKey }) {
  const [loading, setLoading] = useState(false);
  const [summaryData, setSummaryData] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerateSummary = async () => {
    if (!documentId) return;
    setLoading(true);
    setError(null);

    try {
      const data = await summarizePdfApi(documentId, apiKey);
      setSummaryData(data.summary_and_roadmap);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate summary & roadmap.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2>📌 Summary & Actionable Roadmap</h2>
          <p style={{ color: '#94a3b8' }}>Extract key takeaways and structured learning milestones from your document.</p>
        </div>
        <button 
          className="btn" 
          onClick={handleGenerateSummary} 
          disabled={loading || !documentId}
        >
          {loading ? <Loader className="animate-spin" size={18} /> : <Sparkles size={18} />}
          {summaryData ? 'Regenerate Roadmap' : 'Generate Roadmap'}
        </button>
      </div>

      {error && (
        <div style={{ color: '#ef4444', marginBottom: '1rem' }}>
          {error}
        </div>
      )}

      {summaryData ? (
        <div style={{ background: '#0f172a', padding: '1.5rem', borderRadius: '8px', lineHeight: '1.7' }}>
          <ReactMarkdown>{summaryData}</ReactMarkdown>
        </div>
      ) : (
        <div style={{ textAlignment: 'center', padding: '2rem', color: '#94a3b8' }}>
          <FileCheck size={36} style={{ margin: '0 auto 0.5rem', opacity: 0.6 }} />
          <p>Click "Generate Roadmap" to run the Map-Reduce summarization chain over your PDF.</p>
        </div>
      )}
    </div>
  );
}
