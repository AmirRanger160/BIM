import apiClient from './client'
import { mockArticles } from '../data/mockArticles'
import { mockGalleryItems } from '../data/mockGallery'
import { mockTestimonials, mockCertificates, mockStatistics } from '../data/mockData'

// استفاده از API واقعی به طور پیش‌فرض
// mock data فقط به عنوان fallback در صورت خرابی API
const USE_MOCK_DATA = false

// Helper function برای simulating API delay در mock mode
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

// Helper function برای fallback به mock data
const useMockDataFallback = async (mockDataFn) => {
  try {
    return await mockDataFn()
  } catch (error) {
    console.warn('API error, using mock data:', error)
    return null
  }
}

// ============= SLIDERS API =============

/**
 * دریافت یک اسلایدر با تمام تصاویر آن
 * @param {Number} sliderId - شناسه اسلایدر
 * @returns {Promise<Object>} اسلایدر
 */
export const getSlider = async (sliderId) => {
  try {
    if (!sliderId) return { data: null }
    const response = await apiClient.get(`/api/sliders/${sliderId}`)
    return response.data
  } catch (error) {
    console.error('Error fetching slider:', error)
    return { data: null }
  }
}

// ============= ARTICLES API =============

/**
 * دریافت لیست تمام مقالات
 * @param {Object} params - پارامترهای query (category, search, sort, page, limit)
 * @returns {Promise<Array>} لیست مقالات
 */
export const getArticles = async (params = {}) => {
  try {
    // استفاده از API واقعی
    const response = await apiClient.get('/api/articles', { params })
    return response.data
  } catch (error) {
    console.error('Error fetching articles:', error)
    if (USE_MOCK_DATA) {
      await delay(500)
      let filtered = [...mockArticles]
      if (params.category && params.category !== 'همه') {
        filtered = filtered.filter(article => article.category === params.category)
      }
      if (params.search) {
        const searchLower = params.search.toLowerCase()
        filtered = filtered.filter(article => 
          article.title.toLowerCase().includes(searchLower) ||
          article.excerpt.toLowerCase().includes(searchLower) ||
          article.tags.some(tag => tag.toLowerCase().includes(searchLower))
        )
      }
      if (params.sort === 'popular') {
        filtered.sort((a, b) => b.viewsNum - a.viewsNum)
      } else if (params.sort === 'trending') {
        filtered.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0))
      }
      if (params.page && params.limit) {
        const start = (params.page - 1) * params.limit
        const end = start + params.limit
        filtered = filtered.slice(start, end)
      }
      return { data: filtered, total: mockArticles.length }
    }
    throw error
  }
}

/**
 * دریافت یک مقاله با ID
 * @param {Number} id - شناسه مقاله
 * @returns {Promise<Object>} مقاله
 */
export const getArticle = async (id) => {
  try {
    const response = await apiClient.get(`/api/articles/${id}`)
    return response.data
  } catch (error) {
    console.error('Error fetching article:', error)
    if (USE_MOCK_DATA) {
      await delay(300)
      const article = mockArticles.find(a => a.id === parseInt(id))
      if (!article) throw new Error('مقاله یافت نشد')
      return { data: article }
    }
    throw error
  }
}

// Alias for backward compatibility
export const getArticleById = getArticle

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
  try {
    const response = await apiClient.get('/api/gallery', { params })
    return response.data
  } catch (error) {
    console.error('Error fetching gallery items:', error)
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
    throw error
  }
}

/**
 * دریافت یک آیتم گالری با ID
 * @param {Number} id - شناسه آیتم
 * @returns {Promise<Object>} آیتم گالری
 */
export const getGalleryItem = async (id) => {
  try {
    const response = await apiClient.get(`/api/gallery/${id}`)
    return response.data
  } catch (error) {
    console.error('Error fetching gallery item:', error)
    if (USE_MOCK_DATA) {
      await delay(300)
      const item = mockGalleryItems.find(i => i.id === parseInt(id))
      if (!item) throw new Error('آیتم یافت نشد')
      return { data: item }
    }
    throw error
  }
}

// Alias for backward compatibility
export const getGalleryItemById = getGalleryItem

// ============= TESTIMONIALS API =============

/**
 * دریافت لیست نظرات مشتریان
 * @returns {Promise<Array>} لیست نظرات
 */
export const getTestimonials = async () => {
  try {
    const response = await apiClient.get('/api/testimonials')
    return response.data
  } catch (error) {
    console.error('Error fetching testimonials:', error)
    if (USE_MOCK_DATA) {
      await delay(400)
      return { data: mockTestimonials }
    }
    throw error
  }
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
  try {
    const response = await apiClient.get('/api/certificates')
    return response.data
  } catch (error) {
    console.error('Error fetching certificates:', error)
    if (USE_MOCK_DATA) {
      await delay(300)
      return { data: mockCertificates }
    }
    throw error
  }
}

// ============= STATISTICS API =============

/**
 * دریافت آمار سایت
 * @returns {Promise<Array>} لیست آمارها
 */
export const getStatistics = async () => {
  try {
    const response = await apiClient.get('/api/statistics')
    return response.data
  } catch (error) {
    console.error('Error fetching statistics:', error)
    if (USE_MOCK_DATA) {
      await delay(300)
      return { data: mockStatistics }
    }
    throw error
  }
}

// ============= VISITS API =============

export const logVisit = async ({ path, referer }) => {
  try {
    await apiClient.post('/api/visit', {
      path,
      referer: referer || undefined
    })
  } catch (error) {
    // Silent fail to avoid impacting UX
    console.warn('Visit log failed', error?.message || error)
  }
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

export const getVisitSummary = async () => {
  const response = await apiClient.get('/api/admin/visits/summary')
  return response.data
}

export const getVisitReport = async (params = {}) => {
  const response = await apiClient.get('/api/admin/visits/report', { params })
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

// ============= ADMIN CERTIFICATES API =============

/**
 * دریافت تمام گواهینامه‌ها (ادمین)
 * @returns {Promise<Array>} لیست گواهینامه‌ها
 */
export const getAdminCertificates = async () => {
  const response = await apiClient.get('/api/admin/certificates')
  return response.data
}

/**
 * ایجاد گواهینامه جدید (ادمین)
 * @param {Object} certificateData - اطلاعات گواهینامه
 * @returns {Promise<Object>} گواهینامه ایجاد شده
 */
export const createAdminCertificate = async (certificateData) => {
  const response = await apiClient.post('/api/admin/certificates', certificateData)
  return response.data
}

/**
 * بروزرسانی گواهینامه (ادمین)
 * @param {Number} id - شناسه گواهینامه
 * @param {Object} certificateData - اطلاعات جدید
 * @returns {Promise<Object>} گواهینامه بروزرسانی شده
 */
export const updateAdminCertificate = async (id, certificateData) => {
  const response = await apiClient.put(`/api/admin/certificates/${id}`, certificateData)
  return response.data
}

/**
 * حذف گواهینامه (ادمین)
 * @param {Number} id - شناسه گواهینامه
 * @returns {Promise<Object>} پیام موفقیت
 */
export const deleteAdminCertificate = async (id) => {
  const response = await apiClient.delete(`/api/admin/certificates/${id}`)
  return response.data
}

/**
 * دریافت همه خدمات (ادمین)
 * @returns {Promise<Array>} لیست خدمات
 */
export const getAdminServices = async () => {
  const response = await apiClient.get('/api/admin/services')
  return response.data
}

/**
 * ایجاد خدمت جدید (ادمین)
 * @param {Object} serviceData - داده‌های خدمت
 * @returns {Promise<Object>} خدمت ایجادشده
 */
export const createAdminService = async (serviceData) => {
  const response = await apiClient.post('/api/admin/services', serviceData)
  return response.data
}

/**
 * بروزرسانی خدمت (ادمین)
 * @param {Number} id - شناسه خدمت
 * @param {Object} serviceData - داده‌های جدید
 * @returns {Promise<Object>} خدمت بروزرسانی شده
 */
export const updateAdminService = async (id, serviceData) => {
  const response = await apiClient.put(`/api/admin/services/${id}`, serviceData)
  return response.data
}

/**
 * حذف خدمت (ادمین)
 * @param {Number} id - شناسه خدمت
 * @returns {Promise<Object>} نتیجه
 */
export const deleteAdminService = async (id) => {
  const response = await apiClient.delete(`/api/admin/services/${id}`)
  return response.data
}

// ============= ADMIN USERS API =============

/**
 * دریافت همه کاربران (ادمین)
 */
export const getAdminUsers = async () => {
  const response = await apiClient.get('/api/admin/users')
  return response.data
}

/**
 * ایجاد کاربر جدید (ادمین)
 */
export const createAdminUser = async (userData) => {
  const response = await apiClient.post('/api/admin/users', userData)
  return response.data
}

/**
 * بروزرسانی کاربر (ادمین)
 */
export const updateAdminUser = async (id, userData) => {
  const response = await apiClient.put(`/api/admin/users/${id}`, userData)
  return response.data
}

/**
 * حذف کاربر (ادمین)
 */
export const deleteAdminUser = async (id) => {
  const response = await apiClient.delete(`/api/admin/users/${id}`)
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
  deleteSlider: deleteAdminSlider,
  getCertificates: getAdminCertificates,
  createCertificate: createAdminCertificate,
  updateCertificate: updateAdminCertificate,
  deleteCertificate: deleteAdminCertificate,

  // Users
  getUsers: getAdminUsers,
  createUser: createAdminUser,
  updateUser: updateAdminUser,
  deleteUser: deleteAdminUser,

  // Visits
  getVisitSummary,
  getVisitReport,
  
  // Services
  getServices: getAdminServices,
  createService: createAdminService,
  updateService: updateAdminService,
  deleteService: deleteAdminService
}

// ============= COMMENTS API =============

/**
 * دریافت لیست نظرات
 * @param {Object} params - فیلترها (content_type, content_id, approved_only)
 * @returns {Promise<Array>} لیست نظرات
 */
export const getComments = async (params = {}) => {
  try {
    const response = await apiClient.get('/api/comments', { params })
    return response.data
  } catch (error) {
    console.error('Error fetching comments:', error)
    return []
  }
}

/**
 * دریافت یک نظر با شناسه
 * @param {Number} commentId - شناسه نظر
 * @returns {Promise<Object>} نظر
 */
export const getComment = async (commentId) => {
  try {
    const response = await apiClient.get(`/api/comments/${commentId}`)
    return response.data
  } catch (error) {
    console.error('Error fetching comment:', error)
    throw error
  }
}

/**
 * ایجاد نظر جدید
 * @param {Object} commentData - اطلاعات نظر (name, email, content, rating, content_type, content_id)
 * @returns {Promise<Object>} نظر ایجاد شده
 */
export const createComment = async (commentData) => {
  try {
    const response = await apiClient.post('/api/comments', commentData)
    return response.data
  } catch (error) {
    console.error('Error creating comment:', error)
    throw error
  }
}

/**
 * تایید یا رد نظر (فقط ادمین)
 * @param {Number} commentId - شناسه نظر
 * @returns {Promise<Object>} نظر به‌روزرسانی شده
 */
export const approveComment = async (commentId) => {
  try {
    const response = await apiClient.put(`/api/comments/${commentId}/approve`)
    return response.data
  } catch (error) {
    console.error('Error approving comment:', error)
    throw error
  }
}

/**
 * ویرایش نظر (فقط ادمین)
 * @param {Number} commentId - شناسه نظر
 * @param {Object} updateData - اطلاعات جدید (name, email, content, rating, approved)
 * @returns {Promise<Object>} نظر به‌روزرسانی شده
 */
export const updateComment = async (commentId, updateData) => {
  try {
    console.log(`Sending PUT request to /api/comments/${commentId}`, updateData)
    const response = await apiClient.put(`/api/comments/${commentId}`, updateData)
    console.log('Response from updateComment:', response)
    return response.data
  } catch (error) {
    console.error('Error updating comment:', error)
    console.error('Error response:', error.response)
    throw error
  }
}

/**
 * حذف نظر (فقط ادمین)
 * @param {Number} commentId - شناسه نظر
 * @returns {Promise<Object>} پاسخ حذف
 */
export const deleteComment = async (commentId) => {
  try {
    const response = await apiClient.delete(`/api/comments/${commentId}`)
    return response.data
  } catch (error) {
    console.error('Error deleting comment:', error)
    throw error
  }
}

/**
 * دریافت آمار نظرات (فقط ادمین)
 * @returns {Promise<Object>} آمار نظرات
 */
export const getCommentStats = async () => {
  try {
    const response = await apiClient.get('/api/comments/stats/summary')
    return response.data
  } catch (error) {
    console.error('Error fetching comment stats:', error)
    return {
      total: 0,
      approved: 0,
      pending: 0,
      average_rating: 0
    }
  }
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
  logVisit,
  
  // Contact
  sendContactForm,
  subscribeNewsletter,
  
  // Comments
  getComments,
  getComment,
  createComment,
  approveComment,
  updateComment,
  deleteComment,
  getCommentStats
}
