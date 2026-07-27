import React, { useState, useRef } from 'react';
import { uploadPdfApi } from '../api/client';
import { Upload, FileText, CheckCircle, AlertCircle, Loader } from 'lucide-react';

export default function PdfUploader({ apiKey, onPdfUploaded }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fileInfo, setFileInfo] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = async (e) => {
    const file = e.target.files && e.target.files[0];
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
      console.error("Upload error:", err);
      setError(err.response?.data?.detail || err.message || 'Failed to upload PDF file.');
    } finally {
      setLoading(false);
    }
  };

  const handleBoxClick = () => {
    if (fileInputRef.current && !loading) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="card">
      <div 
        className="dropzone" 
        onClick={handleBoxClick} 
        style={{ cursor: 'pointer', touchAction: 'manipulation', padding: '2.5rem 1rem' }}
      >
        <input 
          ref={fileInputRef}
          type="file" 
          accept=".pdf,application/pdf,application/x-pdf" 
          onChange={handleFileChange} 
          id="pdf-input" 
          style={{ display: 'none' }} 
        />
        {loading ? (
          <div>
            <Loader className="animate-spin" size={44} style={{ color: '#6366f1', margin: '0 auto 1rem' }} />
            <h3 style={{ fontSize: '1.1rem' }}>Uploading & Embedding Document...</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>Splitting pages and indexing into Chroma Vector DB...</p>
          </div>
        ) : (
          <div>
            <Upload size={44} style={{ color: '#6366f1', margin: '0 auto 1rem' }} />
            <h3 style={{ fontSize: '1.1rem' }}>Tap here to select PDF file</h3>
            <p style={{ color: '#94a3b8', marginTop: '0.5rem', fontSize: '0.85rem' }}>Supports documents of any size on Mobile & Desktop</p>
          </div>
        )}
      </div>

      {error && (
        <div style={{ marginTop: '1rem', color: '#ef4444', display: 'flex', alignItems: 'center', gap: '0.5rem', background: '#451a1a', padding: '0.75rem 1rem', borderRadius: '8px' }}>
          <AlertCircle size={20} />
          <span style={{ fontSize: '0.9rem' }}>{error}</span>
        </div>
      )}

      {fileInfo && (
        <div style={{ marginTop: '1rem', background: '#0f172a', padding: '1rem', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <FileText size={24} style={{ color: '#34d399' }} />
            <div>
              <strong style={{ color: '#f8fafc', fontSize: '0.95rem' }}>{fileInfo.filename}</strong>
              <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
                {fileInfo.total_pages} Pages • {fileInfo.total_chunks} Chunks
              </div>
            </div>
          </div>
          <span style={{ color: '#34d399', display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.85rem' }}>
            <CheckCircle size={18} /> Indexed
          </span>
        </div>
      )}
    </div>
  );
}
