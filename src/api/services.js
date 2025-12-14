import apiClient from './client'
import { mockArticles } from '../data/mockArticles'
import { mockGalleryItems } from '../data/mockGallery'
import { mockTestimonials, mockCertificates, mockStatistics } from '../data/mockData'

// استفاده از mock data یا API واقعی بر اساس environment variable
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true'

// Helper function برای simulating API delay در mock mode
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

// ============= ARTICLES API =============

/**
 * دریافت لیست تمام مقالات
 * @param {Object} params - پارامترهای query (category, search, sort, page, limit)
 * @returns {Promise<Array>} لیست مقالات
 */
export const getArticles = async (params = {}) => {
  if (USE_MOCK_DATA) {
    await delay(500) // شبیه‌سازی تاخیر شبکه
    let filtered = [...mockArticles]
    
    // فیلتر بر اساس دسته‌بندی
    if (params.category && params.category !== 'همه') {
      filtered = filtered.filter(article => article.category === params.category)
    }
    
    // جستجو
    if (params.search) {
      const searchLower = params.search.toLowerCase()
      filtered = filtered.filter(article => 
        article.title.toLowerCase().includes(searchLower) ||
        article.excerpt.toLowerCase().includes(searchLower) ||
        article.tags.some(tag => tag.toLowerCase().includes(searchLower))
      )
    }
    
    // مرتب‌سازی
    if (params.sort === 'popular') {
      filtered.sort((a, b) => b.viewsNum - a.viewsNum)
    } else if (params.sort === 'trending') {
      filtered.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0))
    }
    
    // Pagination
    if (params.page && params.limit) {
      const start = (params.page - 1) * params.limit
      const end = start + params.limit
      filtered = filtered.slice(start, end)
    }
    
    return { data: filtered, total: mockArticles.length }
  }
  
  // استفاده از API واقعی
  const response = await apiClient.get('/api/articles', { params })
  return response.data
}

/**
 * دریافت یک مقاله با ID
 * @param {Number} id - شناسه مقاله
 * @returns {Promise<Object>} مقاله
 */
export const getArticleById = async (id) => {
  if (USE_MOCK_DATA) {
    await delay(300)
    const article = mockArticles.find(a => a.id === parseInt(id))
    if (!article) throw new Error('مقاله یافت نشد')
    return { data: article }
  }
  
  const response = await apiClient.get(`/api/articles/${id}`)
  return response.data
}

/**
 * ایجاد مقاله جدید (فقط برای ادمین)
 * @param {Object} articleData - اطلاعات مقاله
 * @returns {Promise<Object>} مقاله ایجاد شده
 */
export const createArticle = async (articleData) => {
  const response = await apiClient.post('/api/articles', articleData)
  return response.data
}

/**
 * بروزرسانی مقاله (فقط برای ادمین)
 * @param {Number} id - شناسه مقاله
 * @param {Object} articleData - اطلاعات جدید
 * @returns {Promise<Object>} مقاله بروزرسانی شده
 */
export const updateArticle = async (id, articleData) => {
  const response = await apiClient.put(`/api/articles/${id}`, articleData)
  return response.data
}

/**
 * حذف مقاله (فقط برای ادمین)
 * @param {Number} id - شناسه مقاله
 * @returns {Promise<Object>} پیام موفقیت
 */
export const deleteArticle = async (id) => {
  const response = await apiClient.delete(`/api/articles/${id}`)
  return response.data
}

// ============= GALLERY API =============

/**
 * دریافت لیست آیتم‌های گالری
 * @param {Object} params - پارامترهای query
 * @returns {Promise<Array>} لیست آیتم‌ها
 */
export const getGalleryItems = async (params = {}) => {
  if (USE_MOCK_DATA) {
    await delay(500)
    let filtered = [...mockGalleryItems]
    
    if (params.category && params.category !== 'همه') {
      filtered = filtered.filter(item => item.category === params.category)
    }
    
    if (params.search) {
      const searchLower = params.search.toLowerCase()
      filtered = filtered.filter(item =>
        item.title.toLowerCase().includes(searchLower) ||
        item.description.toLowerCase().includes(searchLower) ||
        item.technologies.some(tech => tech.toLowerCase().includes(searchLower))
      )
    }
    
    return { data: filtered, total: mockGalleryItems.length }
  }
  
  const response = await apiClient.get('/api/gallery', { params })
  return response.data
}

/**
 * دریافت یک آیتم گالری با ID
 * @param {Number} id - شناسه آیتم
 * @returns {Promise<Object>} آیتم گالری
 */
export const getGalleryItemById = async (id) => {
  if (USE_MOCK_DATA) {
    await delay(300)
    const item = mockGalleryItems.find(i => i.id === parseInt(id))
    if (!item) throw new Error('آیتم یافت نشد')
    return { data: item }
  }
  
  const response = await apiClient.get(`/api/gallery/${id}`)
  return response.data
}

// ============= TESTIMONIALS API =============

/**
 * دریافت لیست نظرات مشتریان
 * @returns {Promise<Array>} لیست نظرات
 */
export const getTestimonials = async () => {
  if (USE_MOCK_DATA) {
    await delay(400)
    return { data: mockTestimonials }
  }
  
  const response = await apiClient.get('/api/testimonials')
  return response.data
}

/**
 * ارسال نظر جدید
 * @param {Object} testimonialData - اطلاعات نظر
 * @returns {Promise<Object>} نظر ثبت شده
 */
export const createTestimonial = async (testimonialData) => {
  const response = await apiClient.post('/api/testimonials', testimonialData)
  return response.data
}

// ============= CERTIFICATES API =============

/**
 * دریافت لیست گواهینامه‌ها
 * @returns {Promise<Array>} لیست گواهینامه‌ها
 */
export const getCertificates = async () => {
  if (USE_MOCK_DATA) {
    await delay(300)
    return { data: mockCertificates }
  }
  
  const response = await apiClient.get('/api/certificates')
  return response.data
}

// ============= STATISTICS API =============

/**
 * دریافت آمار سایت
 * @returns {Promise<Array>} لیست آمارها
 */
export const getStatistics = async () => {
  if (USE_MOCK_DATA) {
    await delay(300)
    return { data: mockStatistics }
  }
  
  const response = await apiClient.get('/api/statistics')
  return response.data
}

// ============= CONTACT API =============

/**
 * ارسال فرم تماس
 * @param {Object} contactData - اطلاعات فرم (name, email, subject, message)
 * @returns {Promise<Object>} پیام موفقیت
 */
export const sendContactForm = async (contactData) => {
  if (USE_MOCK_DATA) {
    await delay(800)
    console.log('Contact form submitted (mock):', contactData)
    return { 
      data: { 
        success: true, 
        message: 'پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.' 
      } 
    }
  }
  
  const response = await apiClient.post('/api/contact', contactData)
  return response.data
}

// ============= NEWSLETTER API =============

/**
 * ثبت‌نام در خبرنامه
 * @param {String} email - ایمیل کاربر
 * @returns {Promise<Object>} پیام موفقیت
 */
export const subscribeNewsletter = async (email) => {
  if (USE_MOCK_DATA) {
    await delay(500)
    console.log('Newsletter subscription (mock):', email)
    return { 
      data: { 
        success: true, 
        message: 'ایمیل شما با موفقیت در خبرنامه ثبت شد.' 
      } 
    }
  }
  
  const response = await apiClient.post('/api/newsletter/subscribe', { email })
  return response.data
}

// ============= ADMIN API =============

/**
 * ورود ادمین
 * @param {Object} credentials - {email, password}
 * @returns {Promise<Object>} {access_token, user}
 */
export const adminLogin = async (credentials) => {
  const formData = new URLSearchParams()
  formData.append('username', credentials.email)
  formData.append('password', credentials.password)
  
  const response = await apiClient.post('/api/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
  return response.data
}

/**
 * دریافت آمار داشبورد (ادمین)
 * @returns {Promise<Object>} آمارهای داشبورد
 */
export const getAdminDashboardStats = async () => {
  const response = await apiClient.get('/api/admin/dashboard/stats')
  return response.data
}

/**
 * دریافت تمام مقالات (ادمین)
 * @returns {Promise<Array>} لیست مقالات
 */
export const getAdminArticles = async () => {
  const response = await apiClient.get('/api/admin/articles')
  return response.data
}

/**
 * ایجاد مقاله جدید (ادمین)
 * @param {Object} articleData - اطلاعات مقاله
 * @returns {Promise<Object>} مقاله ایجاد شده
 */
export const createAdminArticle = async (articleData) => {
  const response = await apiClient.post('/api/admin/articles', articleData)
  return response.data
}

/**
 * به‌روزرسانی مقاله (ادمین)
 * @param {Number} id - شناسه مقاله
 * @param {Object} articleData - اطلاعات جدید
 * @returns {Promise<Object>} مقاله به‌روز شده
 */
export const updateAdminArticle = async (id, articleData) => {
  const response = await apiClient.put(`/api/admin/articles/${id}`, articleData)
  return response.data
}

/**
 * حذف مقاله (ادمین)
 * @param {Number} id - شناسه مقاله
 * @returns {Promise<Object>} پیام موفقیت
 */
export const deleteAdminArticle = async (id) => {
  const response = await apiClient.delete(`/api/admin/articles/${id}`)
  return response.data
}

/**
 * دریافت تمام آیتم‌های گالری (ادمین)
 * @returns {Promise<Array>} لیست آیتم‌ها
 */
export const getAdminGalleryItems = async () => {
  const response = await apiClient.get('/api/admin/gallery')
  return response.data
}

/**
 * ایجاد آیتم گالری جدید (ادمین)
 * @param {Object} galleryData - اطلاعات آیتم
 * @returns {Promise<Object>} آیتم ایجاد شده
 */
export const createAdminGalleryItem = async (galleryData) => {
  const response = await apiClient.post('/api/admin/gallery', galleryData)
  return response.data
}

/**
 * به‌روزرسانی آیتم گالری (ادمین)
 * @param {Number} id - شناسه آیتم
 * @param {Object} galleryData - اطلاعات جدید
 * @returns {Promise<Object>} آیتم به‌روز شده
 */
export const updateAdminGalleryItem = async (id, galleryData) => {
  const response = await apiClient.put(`/api/admin/gallery/${id}`, galleryData)
  return response.data
}

/**
 * حذف آیتم گالری (ادمین)
 * @param {Number} id - شناسه آیتم
 * @returns {Promise<Object>} پیام موفقیت
 */
export const deleteAdminGalleryItem = async (id) => {
  const response = await apiClient.delete(`/api/admin/gallery/${id}`)
  return response.data
}

/**
 * دریافت تمام نظرات (ادمین)
 * @returns {Promise<Array>} لیست نظرات
 */
export const getAdminTestimonials = async () => {
  const response = await apiClient.get('/api/admin/testimonials')
  return response.data
}

/**
 * ایجاد نظر جدید (ادمین)
 * @param {Object} testimonialData - اطلاعات نظر
 * @returns {Promise<Object>} نظر ایجاد شده
 */
export const createAdminTestimonial = async (testimonialData) => {
  const response = await apiClient.post('/api/admin/testimonials', testimonialData)
  return response.data
}

/**
 * به‌روزرسانی نظر (ادمین)
 * @param {Number} id - شناسه نظر
 * @param {Object} testimonialData - اطلاعات جدید
 * @returns {Promise<Object>} نظر به‌روز شده
 */
export const updateAdminTestimonial = async (id, testimonialData) => {
  const response = await apiClient.put(`/api/admin/testimonials/${id}`, testimonialData)
  return response.data
}

/**
 * تایید نظر (ادمین)
 * @param {Number} id - شناسه نظر
 * @returns {Promise<Object>} پیام موفقیت
 */
export const approveAdminTestimonial = async (id) => {
  const response = await apiClient.patch(`/api/admin/testimonials/${id}/approve`)
  return response.data
}

/**
 * حذف نظر (ادمین)
 * @param {Number} id - شناسه نظر
 * @returns {Promise<Object>} پیام موفقیت
 */
export const deleteAdminTestimonial = async (id) => {
  const response = await apiClient.delete(`/api/admin/testimonials/${id}`)
  return response.data
}

/**
 * دریافت تمام پیام‌های تماس (ادمین)
 * @returns {Promise<Array>} لیست پیام‌ها
 */
export const getAdminContacts = async () => {
  const response = await apiClient.get('/api/admin/contacts')
  return response.data
}

/**
 * علامت‌گذاری پیام به عنوان خوانده شده (ادمین)
 * @param {Number} id - شناسه پیام
 * @returns {Promise<Object>} پیام موفقیت
 */
export const markAdminContactRead = async (id) => {
  const response = await apiClient.patch(`/api/admin/contacts/${id}/read`)
  return response.data
}

/**
 * حذف پیام تماس (ادمین)
 * @param {Number} id - شناسه پیام
 * @returns {Promise<Object>} پیام موفقیت
 */
export const deleteAdminContact = async (id) => {
  const response = await apiClient.delete(`/api/admin/contacts/${id}`)
  return response.data
}

/**
 * آپلود فایل (عکس)
 * @param {FormData} formData - فایل را در FormData قرار دهید
 * @returns {Promise<Object>} {url}
 */
export const uploadFile = async (formData) => {
  const response = await apiClient.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

// ============= ADMIN SLIDERS API =============

/**
 * دریافت تمام اسلایدرها (ادمین)
 * @returns {Promise<Array>} لیست اسلایدرها
 */
export const getAdminSliders = async () => {
  const response = await apiClient.get('/api/admin/sliders')
  return response.data
}

/**
 * ایجاد اسلایدر جدید (ادمین)
 * @param {Object} sliderData - داده‌های اسلایدر
 * @returns {Promise<Object>} اسلایدر ایجادشده
 */
export const createAdminSlider = async (sliderData) => {
  const response = await apiClient.post('/api/admin/sliders', sliderData)
  return response.data
}

/**
 * بروزرسانی اسلایدر (ادمین)
 * @param {Number} id - شناسه اسلایدر
 * @param {Object} sliderData - داده‌های جدید
 * @returns {Promise<Object>} اسلایدر بروزرسانی‌شده
 */
export const updateAdminSlider = async (id, sliderData) => {
  const response = await apiClient.put(`/api/admin/sliders/${id}`, sliderData)
  return response.data
}

/**
 * حذف اسلایدر (ادمین)
 * @param {Number} id - شناسه اسلایدر
 * @returns {Promise<Object>} پیام موفقیت
 */
export const deleteAdminSlider = async (id) => {
  const response = await apiClient.delete(`/api/admin/sliders/${id}`)
  return response.data
}

// Export admin service
export const adminService = {
  login: adminLogin,
  uploadFile: uploadFile,
  getDashboardStats: getAdminDashboardStats,
  getArticles: getAdminArticles,
  createArticle: createAdminArticle,
  updateArticle: updateAdminArticle,
  deleteArticle: deleteAdminArticle,
  getGalleryItems: getAdminGalleryItems,
  createGalleryItem: createAdminGalleryItem,
  updateGalleryItem: updateAdminGalleryItem,
  deleteGalleryItem: deleteAdminGalleryItem,
  getTestimonials: getAdminTestimonials,
  createTestimonial: createAdminTestimonial,
  updateTestimonial: updateAdminTestimonial,
  approveTestimonial: approveAdminTestimonial,
  deleteTestimonial: deleteAdminTestimonial,
  getContacts: getAdminContacts,
  markContactRead: markAdminContactRead,
  deleteContact: deleteAdminContact,
  getSliders: getAdminSliders,
  createSlider: createAdminSlider,
  updateSlider: updateAdminSlider,
  deleteSlider: deleteAdminSlider
}

// Export all services as default
export default {
  // Admin
  adminService,
  
  // Articles
  getArticles,
  getArticleById,
  createArticle,
  updateArticle,
  deleteArticle,
  
  // Gallery
  getGalleryItems,
  getGalleryItemById,
  
  // Testimonials
  getTestimonials,
  createTestimonial,
  
  // Certificates
  getCertificates,
  
  // Statistics
  getStatistics,
  
  // Contact
  sendContactForm,
  subscribeNewsletter
}
