import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 responses
api.interceptors.response.use(
  (response) => {
    console.log('API Response Success:', response.config.url, response.status);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.config?.url, error.response?.status, error.message);
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token');
      if (window.location.pathname.startsWith('/admin') && !window.location.pathname.includes('/login')) {
        window.history.pushState(null, '', '/admin/login');
        window.dispatchEvent(new PopStateEvent('popstate'));
      }
    }
    return Promise.reject(error);
  }
);

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

export const adminAuthService = {
  login: (credentials) => api.post('/auth/login', credentials),
  getCurrentUser: () => api.get('/auth/me'),
};

// Admin services for content management
export const adminArticleService = {
  getAll: (params = {}) => api.get('/articles', { params }),
  getById: (id) => api.get(`/articles/${id}`),
  create: (data) => api.post('/articles', data),
  update: (id, data) => api.put(`/articles/${id}`, data),
  delete: (id) => api.delete(`/articles/${id}`),
};

export const adminProjectService = {
  getAll: (params = {}) => api.get('/projects', { params }),
  getById: (id) => api.get(`/projects/${id}`),
  create: (data) => api.post('/projects', data),
  update: (id, data) => api.put(`/projects/${id}`, data),
  delete: (id) => api.delete(`/projects/${id}`),
};

export const adminServiceService = {
  getAll: (params = {}) => api.get('/services', { params }),
  getById: (id) => api.get(`/services/${id}`),
  create: (data) => api.post('/services', data),
  update: (id, data) => api.put(`/services/${id}`, data),
  delete: (id) => api.delete(`/services/${id}`),
};

export const adminTeamService = {
  getAll: (params = {}) => api.get('/team', { params }),
  getById: (id) => api.get(`/team/${id}`),
  create: (data) => api.post('/team', data),
  update: (id, data) => api.put(`/team/${id}`, data),
  delete: (id) => api.delete(`/team/${id}`),
};

export const adminCertificateService = {
  getAll: (params = {}) => api.get('/certificates', { params }),
  getById: (id) => api.get(`/certificates/${id}`),
  create: (data) => api.post('/certificates', data),
  update: (id, data) => api.put(`/certificates/${id}`, data),
  delete: (id) => api.delete(`/certificates/${id}`),
};

export const adminLicenseService = {
  getAll: (params = {}) => api.get('/licenses', { params }),
  getById: (id) => api.get(`/licenses/${id}`),
  create: (data) => api.post('/licenses', data),
  update: (id, data) => api.put(`/licenses/${id}`, data),
  delete: (id) => api.delete(`/licenses/${id}`),
};

export const adminContactService = {
  getAll: (params = {}) => api.get('/contact/admin/contact-submissions', { params }),
  getById: (id) => api.get(`/contact/admin/contact-submissions/${id}`),
  updateStatus: (id, status) => api.patch(`/contact/admin/contact-submissions/${id}/status`, { status }),
  delete: (id) => api.delete(`/contact/admin/contact-submissions/${id}`),
};

export const adminSettingsService = {
  getCompanyInfo: () => api.get('/contact/company-info'),
  updateCompanyInfo: (data) => api.put('/contact/admin/company-info', data),
  getStatistics: () => api.get('/contact/statistics'),
  updateStatistics: (data) => api.put('/contact/admin/statistics', data),
};

export default api;
