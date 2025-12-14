import axios from 'axios'

// API Base URL from environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT || 30000

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor - برای اضافه کردن token و سایر headers
apiClient.interceptors.request.use(
  (config) => {
    // اگر token ادمین داشتید، اضافه کنید
    const adminToken = localStorage.getItem('admin_token')
    const authToken = localStorage.getItem('auth_token')
    
    if (adminToken) {
      config.headers.Authorization = `Bearer ${adminToken}`
    } else if (authToken) {
      config.headers.Authorization = `Bearer ${authToken}`
    }
    
    // تنظیم content-type اگر URLSearchParams است
    if (config.data instanceof URLSearchParams) {
      config.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - برای مدیریت خطاها
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // مدیریت خطاهای مختلف
    if (error.response) {
      // سرور پاسخ با خطا داده
      switch (error.response.status) {
        case 401:
          console.error('Unauthorized - لطفا دوباره وارد شوید')
          // می‌توانید کاربر را به صفحه لاگین هدایت کنید
          break
        case 403:
          console.error('Forbidden - دسترسی ندارید')
          break
        case 404:
          console.error('Not Found - منبع مورد نظر یافت نشد')
          break
        case 500:
          console.error('Server Error - خطا در سرور')
          break
        default:
          console.error('API Error:', error.response.data)
      }
    } else if (error.request) {
      // درخواست ارسال شده ولی پاسخی دریافت نشده
      console.error('Network Error - لطفا اتصال اینترنت را بررسی کنید')
    } else {
      // خطایی در تنظیم درخواست رخ داده
      console.error('Error:', error.message)
    }
    return Promise.reject(error)
  }
)

export default apiClient
