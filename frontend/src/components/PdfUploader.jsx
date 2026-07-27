import React, { useState, useRef } from 'react';
import { uploadPdfApi } from '../api/client';
import { Upload, FileText, CheckCircle, AlertOctagon, Loader } from 'lucide-react';

export default function PdfUploader({ apiKey, onPdfUploaded }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fileInfo, setFileInfo] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = async (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('PDF Cannot Be Embedded: Only PDF documents (.pdf) are supported.');
      return;
    }

    // Client-side file size pre-audit (50MB limit)
    const maxSizeBytes = 50 * 1024 * 1024;
    if (file.size > maxSizeBytes) {
      const fileSizeMb = (file.size / (1024 * 1024)).toFixed(2);
      setError(`PDF Cannot Be Embedded: File size (${fileSizeMb} MB) exceeds maximum allowed limit of 50 MB.`);
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
      setError(err.response?.data?.detail || err.message || 'PDF Cannot Be Embedded: Upload or parsing failed.');
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
            <h3 style={{ fontSize: '1.1rem' }}>Auditing & Embedding PDF Document...</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>Validating text extractability and indexing into Chroma Vector DB...</p>
          </div>
        ) : (
          <div>
            <Upload size={44} style={{ color: '#6366f1', margin: '0 auto 1rem' }} />
            <h3 style={{ fontSize: '1.1rem' }}>Tap here or Drag & Drop PDF to Audit & Embed</h3>
            <p style={{ color: '#94a3b8', marginTop: '0.5rem', fontSize: '0.85rem' }}>Max file size: 50 MB • Max pages: 200 • Text PDFs supported</p>
          </div>
        )}
      </div>

      {/* Prominent Red Alert Component for Failed PDF Audits */}
      {error && (
        <div style={{ 
          marginTop: '1.25rem', 
          background: 'rgba(239, 68, 68, 0.15)', 
          border: '1.5px solid #ef4444', 
          padding: '1rem 1.25rem', 
          borderRadius: '10px', 
          display: 'flex', 
          alignItems: 'flex-start', 
          gap: '0.75rem' 
        }}>
          <AlertOctagon size={24} style={{ color: '#ef4444', flexShrink: 0, marginTop: '2px' }} />
          <div>
            <strong style={{ color: '#fca5a5', display: 'block', fontSize: '1rem', marginBottom: '0.25rem' }}>
              ⚠️ THIS PDF CANNOT BE EMBEDDED
            </strong>
            <span style={{ color: '#f8fafc', fontSize: '0.92rem', lineHeight: '1.5' }}>
              {error}
            </span>
          </div>
        </div>
      )}

      {fileInfo && (
        <div style={{ marginTop: '1rem', background: '#0f172a', padding: '1rem', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <FileText size={24} style={{ color: '#34d399' }} />
            <div>
              <strong style={{ color: '#f8fafc', fontSize: '0.95rem' }}>{fileInfo.filename}</strong>
              <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
                {fileInfo.total_pages} Pages • {fileInfo.total_chunks} Vector Chunks (Audit Passed)
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
