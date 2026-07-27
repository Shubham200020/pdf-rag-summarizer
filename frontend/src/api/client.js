import axios from 'axios';

export const getApiBaseUrl = () => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  // Check custom backend URL stored in localStorage
  const customBackend = localStorage.getItem('custom_backend_url');
  if (customBackend) {
    return customBackend.endsWith('/api') ? customBackend : `${customBackend.replace(/\/$/, '')}/api`;
  }
  // If hosted on GitHub Pages static host, connect to active backend tunnel
  if (typeof window !== 'undefined' && window.location.hostname.includes('github.io')) {
    return 'https://eighty-feet-unite.loca.lt/api';
  }
  return '/api';
};

export const uploadPdfApi = async (file, apiKey = '') => {
  const formData = new FormData();
  formData.append('file', file);
  if (apiKey) {
    formData.append('api_key', apiKey);
  }
  
  const baseUrl = getApiBaseUrl();
  const response = await axios.post(`${baseUrl}/pdf/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const summarizePdfApi = async (documentId, apiKey = '', modelName = 'gpt-4o-mini') => {
  const baseUrl = getApiBaseUrl();
  const response = await axios.post(`${baseUrl}/pdf/summarize`, {
    document_id: documentId,
    model_name: modelName,
    api_key: apiKey || null
  });
  return response.data;
};

export const queryChatApi = async (documentId, question, apiKey = '', modelName = 'gpt-4o-mini') => {
  const baseUrl = getApiBaseUrl();
  const response = await axios.post(`${baseUrl}/chat/query`, {
    document_id: documentId,
    question: question,
    model_name: modelName,
    api_key: apiKey || null
  });
  return response.data;
};
