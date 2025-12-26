import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Event emitter for error notifications
export const apiErrorEmitter = {
  listeners: [],
  on(callback) {
    this.listeners.push(callback);
  },
  off(callback) {
    this.listeners = this.listeners.filter(l => l !== callback);
  },
  emit(error) {
    this.listeners.forEach(callback => callback(error));
  }
};

// Track refresh token request to avoid multiple simultaneous requests
let isRefreshing = false;
let refreshSubscribers = [];

const onRefreshed = (token) => {
  refreshSubscribers.forEach(callback => callback(token));
  refreshSubscribers = [];
};

const addRefreshSubscriber = (callback) => {
  refreshSubscribers.push(callback);
};

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

// Handle responses with comprehensive error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response Success:', response.config.url, response.status);
    return response;
  },
  async (error) => {
    const config = error.config;
    
    console.error('API Response Error:', config?.url, error.response?.status, error.message);
    
    // Handle 401 Unauthorized - attempt token refresh
    if (error.response?.status === 401 && !config._retry) {
      config._retry = true;
      
      if (isRefreshing) {
        return new Promise((resolve) => {
          addRefreshSubscriber((token) => {
            config.headers.Authorization = `Bearer ${token}`;
            resolve(api(config));
          });
        });
      }
      
      isRefreshing = true;
      
      try {
        // Attempt to refresh token by re-logging in (simple approach)
        // In a production app, you'd have a refresh token endpoint
        localStorage.removeItem('admin_token');
        isRefreshing = false;
        onRefreshed(null);
        
        // Redirect to login
        if (window.location.pathname.startsWith('/admin') && !window.location.pathname.includes('/login')) {
          apiErrorEmitter.emit({
            type: 'auth_expired',
            message: 'Session expired. Please login again.'
          });
          window.history.pushState(null, '', '/admin/login');
          window.dispatchEvent(new PopStateEvent('popstate'));
        }
      } catch (err) {
        isRefreshing = false;
        apiErrorEmitter.emit({
          type: 'refresh_error',
          message: 'Failed to refresh session'
        });
      }
    }
    
    // Emit error for UI notification
    if (error.response) {
      const message = error.response.data?.detail || 
                     error.response.data?.message || 
                     `Error: ${error.response.status}`;
      
      apiErrorEmitter.emit({
        type: 'api_error',
        status: error.response.status,
        message
      });
    } else if (error.request) {
      apiErrorEmitter.emit({
        type: 'network_error',
        message: 'Network error. Please check your connection.'
      });
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
  submit: (data) => api.post('/contact', data),
  getCompanyInfo: () => api.get('/contact/company-info'),
};

export const authService = {
  login: (credentials) => api.post('/auth/login', credentials),
};

export const uploadService = {
  uploadImage: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
  }
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
  create: (data) => {
    try {
      console.debug('adminProjectService.create payload:', data);
    } catch (e) {}
    return api.post('/projects', data);
  },
  update: (id, data) => {
    try {
      console.debug('adminProjectService.update payload:', { id, ...data });
    } catch (e) {}
    return api.put(`/projects/${id}`, data);
  },
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

export const adminUserService = {
  getAll: () => api.get('/users'),
  create: (data) => api.post('/users', data),
  update: (id, data) => api.put(`/users/${id}`, data),
  delete: (id) => api.delete(`/users/${id}`),
};

export default api;
