import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

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
