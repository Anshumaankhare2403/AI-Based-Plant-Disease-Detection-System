/**
 * PlantCare AI - API Service Layer
 * Centralized Axios client for all backend REST endpoints.
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Accept': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor to attach active user token/ID if present
apiClient.interceptors.request.use((config) => {
  try {
    const savedUser = localStorage.getItem('plantcare_user');
    if (savedUser) {
      const user = JSON.parse(savedUser);
      if (user?.id) {
        config.headers['X-User-Id'] = user.id;
      }
    }
  } catch (e) {
    // Ignore JSON parse errors
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const apiService = {
  // System Health
  async getHealth() {
    const res = await apiClient.get('/health');
    return res.data;
  },

  // Model Metadata & Metrics
  async getModelInfo() {
    const res = await apiClient.get('/model/info');
    return res.data;
  },

  // Disease Prediction (Image Upload)
  async predictImage(file, onUploadProgress) {
    const formData = new FormData();
    formData.append('image', file);

    const res = await apiClient.post('/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress,
    });
    return res.data;
  },

  // Prediction History
  async getHistory(limit = 50) {
    const res = await apiClient.get('/history', {
      params: { limit },
    });
    return res.data;
  },

  // Analytics & Dashboard Stats
  async getDashboardStats() {
    const res = await apiClient.get('/dashboard/stats');
    return res.data;
  },

  // Auth: Register
  async register(email, password, displayName) {
    const res = await apiClient.post('/auth/register', {
      email,
      password,
      display_name: displayName,
    });
    return res.data;
  },

  // Auth: Login
  async login(email, password) {
    const res = await apiClient.post('/auth/login', {
      email,
      password,
    });
    return res.data;
  },

  // Auth: Service status
  async getAuthStatus() {
    const res = await apiClient.get('/auth/status');
    return res.data;
  },
};

export default apiClient;

