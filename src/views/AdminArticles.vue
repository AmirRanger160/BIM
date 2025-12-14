<template>
  <div class="admin-articles">
    <div class="header-actions">
      <button @click="showForm = true" class="btn-primary">
        ➕ مقاله جدید
      </button>
    </div>

    <!-- فرم افزودن/ویرایش -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal-card">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش مقاله' : 'مقاله جدید' }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="submitForm" class="article-form">
          <div class="form-row">
            <div class="form-group">
              <label>عنوان</label>
              <input v-model="formData.title" type="text" required />
            </div>
            <div class="form-group">
              <label>نویسنده</label>
              <input v-model="formData.author" type="text" required />
            </div>
          </div>

          <div class="form-group">
            <label>خلاصه</label>
            <textarea v-model="formData.excerpt" rows="3" required></textarea>
          </div>

          <div class="form-group">
            <label>محتوای کامل</label>
            <textarea v-model="formData.full_content" rows="6" required></textarea>
          </div>

          <div class="form-group">
            <label>دسته‌بندی</label>
            <input v-model="formData.category" type="text" required />
          </div>

          <div class="form-group">
            <label>تصویر شاخص</label>
            <div class="file-input-group">
              <input 
                type="file" 
                @change="handleImageUpload" 
                accept="image/*"
                class="file-input"
              />
              <input v-model="formData.image" type="text" placeholder="یا URL تصویر را پیوند کنید" />
            </div>
            <div v-if="uploadingImage" class="uploading-status">درحال آپلود...</div>
          </div>

          <div class="form-group">
            <label>اسلایدر (چندین عکس)</label>
            <select v-model="formData.slider_id">
              <option :value="null">-- انتخاب نکنید --</option>
              <option v-for="slider in sliders" :key="slider.id" :value="slider.id">
                {{ slider.name }} ({{ slider.images?.length || 0 }} عکس)
              </option>
            </select>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ editingId ? 'ذخیره تغییرات' : 'ایجاد مقاله' }}</button>
            <button type="button" @click="closeForm" class="btn-secondary">انصراف</button>
          </div>
        </form>
      </div>
    </div>

    <!-- لیست مقالات -->
    <div class="articles-list">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="articles.length === 0" class="empty">
        <p>هیچ مقاله‌ای یافت نشد</p>
      </div>
      <div v-else>
        <div class="table-wrapper">
          <table class="articles-table">
            <thead>
              <tr>
                <th>عنوان</th>
                <th>نویسنده</th>
                <th>دسته‌بندی</th>
                <th>تاریخ ایجاد</th>
                <th>عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="article in articles" :key="article.id">
                <td>{{ article.title }}</td>
                <td>{{ article.author }}</td>
                <td>{{ article.category }}</td>
                <td>{{ formatDate(article.created_at) }}</td>
                <td class="actions">
                  <button @click="editArticle(article)" class="btn-edit">✏️</button>
                  <button @click="deleteArticle(article.id)" class="btn-delete">🗑️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminService } from '../api/services'

const articles = ref([])
const sliders = ref([])
const loading = ref(false)
const showForm = ref(false)
const editingId = ref(null)
const uploadingImage = ref(false)
const formData = ref({
  title: '',
  excerpt: '',
  full_content: '',
  category: '',
  author: '',
  image: '',
  slider_id: null
})

const loadArticles = async () => {
  loading.value = true
  try {
    articles.value = await adminService.getArticles()
    sliders.value = await adminService.getSliders()
  } catch (error) {
    console.error('Failed to load articles:', error)
    alert('خطا در بارگذاری مقالات')
  } finally {
    loading.value = false
  }
}

const editArticle = (article) => {
  editingId.value = article.id
  formData.value = { ...article }
  showForm.value = true
}

const submitForm = async () => {
  try {
    if (editingId.value) {
      await adminService.updateArticle(editingId.value, formData.value)
      alert('مقاله با موفقیت به‌روزرسانی شد')
    } else {
      await adminService.createArticle(formData.value)
      alert('مقاله با موفقیت ایجاد شد')
    }
    closeForm()
    await loadArticles()
  } catch (error) {
    alert('خطا: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  }
}

const deleteArticle = async (id) => {
  if (!confirm('آیا از حذف این مقاله مطمئن هستید؟')) return
  
  try {
    await adminService.deleteArticle(id)
    alert('مقاله با موفقیت حذف شد')
    await loadArticles()
  } catch (error) {
    alert('خطا: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  }
}

const closeForm = () => {
  showForm.value = false
  editingId.value = null
  formData.value = {
    title: '',
    excerpt: '',
    full_content: '',
    category: '',
    author: '',
    image: '',
    slider_id: null
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('fa-IR')
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  uploadingImage.value = true
  try {
    const formDataFile = new FormData()
    formDataFile.append('file', file)
    const response = await adminService.uploadFile(formDataFile)
    formData.value.image = response.url
  } catch (error) {
    alert('خطا در آپلود تصویر: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  } finally {
    uploadingImage.value = false
  }
}

onMounted(() => {
  loadArticles()
})
</script>

<style scoped>
.admin-articles {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-card {
  background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 {
  margin: 0;
  color: #2d3748;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #718096;
}

.article-form {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #2d3748;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.95rem;
  color: #2d3748;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.file-input-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.file-input {
  padding: 0.75rem;
  border: 2px dashed #667eea;
  border-radius: 6px;
  cursor: pointer;
  background: #f7fafc;
  color: #2d3748;
}

.file-input:hover {
  background: #edf2f7;
}

.uploading-status {
  color: #667eea;
  font-size: 0.85rem;
  font-weight: 500;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: #e2e8f0;
  color: #2d3748;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: #cbd5e0;
}

.articles-list {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.loading,
.empty {
  padding: 3rem;
  text-align: center;
  color: #718096;
  background: white;
}

.table-wrapper {
  overflow-x: auto;
}

.articles-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.articles-table thead {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.articles-table th {
  padding: 1rem;
  text-align: right;
  font-weight: 700;
  color: white;
  border-bottom: 2px solid #667eea;
  font-size: 0.95rem;
}

.articles-table td {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
  color: #2d3748;
  background: white;
}

.articles-table tbody tr:hover {
  background: #f7fafc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit,
.btn-delete {
  padding: 0.5rem 0.75rem;
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.btn-edit:hover {
  background: #edf2f7;
  border-color: #667eea;
}

.btn-delete:hover {
  background: #fff5f5;
  border-color: #e53e3e;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-card {
    width: 95%;
  }
}
</style>
