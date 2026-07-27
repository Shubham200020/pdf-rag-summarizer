import React, { useState } from 'react';
import { uploadPdfApi } from '../api/client';
import { Upload, FileText, CheckCircle, AlertCircle, Loader } from 'lucide-react';

export default function PdfUploader({ apiKey, onPdfUploaded }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fileInfo, setFileInfo] = useState(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Please select a valid PDF document.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await uploadPdfApi(file, apiKey);
      setFileInfo(data);
      if (onPdfUploaded) {
        onPdfUploaded(data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload PDF file.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="dropzone">
        <input 
          type="file" 
          accept="application/pdf" 
          onChange={handleFileChange} 
          id="pdf-input" 
          style={{ display: 'none' }} 
        />
        <label htmlFor="pdf-input" style={{ cursor: 'pointer', display: 'block' }}>
          {loading ? (
            <div>
              <Loader className="animate-spin" size={48} style={{ color: '#6366f1', margin: '0 auto 1rem' }} />
              <h3>Uploading & Embedding Document...</h3>
              <p style={{ color: '#94a3b8' }}>Splitting pages and indexing into Chroma Vector DB...</p>
            </div>
          ) : (
            <div>
              <Upload size={48} style={{ color: '#6366f1', margin: '0 auto 1rem' }} />
              <h3>Drag & Drop your PDF here, or <span style={{ color: '#818cf8', textDecoration: 'underline' }}>Browse File</span></h3>
              <p style={{ color: '#94a3b8', marginTop: '0.5rem' }}>Supports documents of any size</p>
            </div>
          )}
        </label>
      </div>

      {error && (
        <div style={{ marginTop: '1rem', color: '#ef4444', display: 'flex', alignItems: 'center', gap: '0.5rem', background: '#451a1a', padding: '0.75rem 1rem', borderRadius: '8px' }}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {fileInfo && (
        <div style={{ marginTop: '1rem', background: '#0f172a', padding: '1rem', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <FileText size={24} style={{ color: '#34d399' }} />
            <div>
              <strong style={{ color: '#f8fafc' }}>{fileInfo.filename}</strong>
              <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
                {fileInfo.total_pages} Pages • {fileInfo.total_chunks} Vector Chunks
              </div>
            </div>
          </div>
          <span style={{ color: '#34d399', display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.9rem' }}>
            <CheckCircle size={18} /> Indexed
          </span>
        </div>
      )}
    </div>
  );
}
