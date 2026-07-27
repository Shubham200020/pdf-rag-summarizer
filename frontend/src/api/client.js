import axios from 'axios';

// Use relative '/api' path by default so mobile browsers & production deployments route to the server origin automatically
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export const uploadPdfApi = async (file, apiKey = '') => {
  const formData = new FormData();
  formData.append('file', file);
  if (apiKey) {
    formData.append('api_key', apiKey);
  }
  
  const response = await axios.post(`${API_BASE_URL}/pdf/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const summarizePdfApi = async (documentId, apiKey = '', modelName = 'gpt-4o-mini') => {
  const response = await axios.post(`${API_BASE_URL}/pdf/summarize`, {
    document_id: documentId,
    model_name: modelName,
    api_key: apiKey || null
  });
  return response.data;
};

export const queryChatApi = async (documentId, question, apiKey = '', modelName = 'gpt-4o-mini') => {
  const response = await axios.post(`${API_BASE_URL}/chat/query`, {
    document_id: documentId,
    question: question,
    model_name: modelName,
    api_key: apiKey || null
  });
  return response.data;
};
