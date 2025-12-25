import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const projectService = {
  getAll: (params = {}) => api.get('/projects', { params }),
  getBySlug: (slug) => api.get(`/projects/${slug}`),
};

export const articleService = {
  getAll: (params = {}) => api.get('/articles', { params }),
  getBySlug: (slug) => api.get(`/articles/${slug}`),
};

export const teamService = {
  getAll: () => api.get('/team'),
};

export const serviceService = {
  getAll: (params = {}) => api.get('/services', { params }),
};

export const certificateService = {
  getAll: () => api.get('/certificates'),
};

export const licenseService = {
  getAll: () => api.get('/licenses'),
};

export const contactService = {
  submit: (data) => api.post('/contact/submit', data),
  getCompanyInfo: () => api.get('/contact'),
};

export const authService = {
  login: (credentials) => api.post('/auth/login', credentials),
};

export default api;
