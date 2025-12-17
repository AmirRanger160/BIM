<template>
  <div class="admin-articles admin-page">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">📝 مدیریت مقالات</div>
        <h2>مقالات</h2>
        <p class="muted">ایجاد، ویرایش و مدیریت انتشار مقالات سایت</p>
        <div class="meta-chips">
          <span class="chip">{{ articles.length }} مقاله</span>
          <span class="chip subtle" v-if="sliders.length">{{ sliders.length }} اسلایدر موجود</span>
        </div>
      </div>
      <div class="header-actions">
        <button @click="showForm = true" class="btn-primary ghost">
          ➕ مقاله جدید
        </button>
      </div>
    </div>

    <!-- فرم افزودن/ویرایش -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal-card large-modal">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش مقاله' : 'مقاله جدید' }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="submitForm" class="article-form">
          <!-- Row 1: Title -->
          <div class="form-group full">
            <label>عنوان مقاله</label>
            <input v-model="formData.title" type="text" placeholder="عنوان جذاب و توصیفی" required />
          </div>

          <!-- Row 2: Author & Category -->
          <div class="form-row">
            <div class="form-group">
              <label>نویسنده</label>
              <input v-model="formData.author" type="text" placeholder="نام نویسنده" required />
            </div>
            <div class="form-group">
              <label>دسته‌بندی</label>
              <input v-model="formData.category" type="text" placeholder="مثلاً: تکنولوژی" required />
            </div>
          </div>

          <!-- Row 3: Excerpt -->
          <div class="form-group full">
            <label>خلاصه (درج‌شده در لیست)</label>
            <textarea v-model="formData.excerpt" rows="3" placeholder="خلاصه کوتاه که در صفحه آرشیو نمایش داده می‌شود"></textarea>
          </div>

          <!-- Row 4: Rich Text Editor -->
          <div class="form-group full">
            <label>محتوای اصلی</label>
            <div class="editor-container">
              <QuillEditor
                v-model:content="formData.full_content"
                theme="snow"
                content-type="html"
              />
            </div>
          </div>

          <!-- Row 5: Image & Slider -->
          <div class="form-row">
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
              <label>اسلایدر (اختیاری)</label>
              <select v-model="formData.slider_id">
                <option :value="null">-- انتخاب نکنید --</option>
                <option v-for="slider in sliders" :key="slider.id" :value="slider.id">
                  {{ slider.name }} ({{ slider.images?.length || 0 }} عکس)
                </option>
              </select>
            </div>
          </div>

          <!-- Form Actions -->
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
          <table class="articles-table frosted-table">
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
                <td><span class="pill">{{ article.category }}</span></td>
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
import { QuillEditor } from '@vueup/vue-quill'
import 'quill/dist/quill.snow.css'
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
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در بارگذاری مقالات'); } catch {}
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
      try { const { success } = await import('../composables/useToast.js'); success('مقاله بروزرسانی شد'); } catch {}
    } else {
      await adminService.createArticle(formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('مقاله ایجاد شد'); } catch {}
    }
    closeForm()
    await loadArticles()
  } catch (error) {
    try { const { error: tError } = await import('../composables/useToast.js'); tError(error.response?.data?.detail || 'خطا در ذخیره مقاله'); } catch {}
  }
}

const deleteArticle = async (id) => {
  if (!confirm('آیا از حذف این مقاله مطمئن هستید؟')) return 
  
  try {
    await adminService.deleteArticle(id)
    try { const { success } = await import('../composables/useToast.js'); success('مقاله حذف شد'); } catch {}
    await loadArticles()
  } catch (error) {
    try { const { error: tError } = await import('../composables/useToast.js'); tError(error.response?.data?.detail || 'خطا در حذف مقاله'); } catch {}
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
    try { const { error: tError } = await import('../composables/useToast.js'); tError(error.response?.data?.detail || 'خطا در آپلود تصویر'); } catch {}
  } finally {
    uploadingImage.value = false
  }
}

onMounted(() => {
  loadArticles()
})
</script>

<style scoped>
/* This view now uses the global admin theme (admin.css) with a few local touches. */
.header-actions { display: flex; gap: 1rem; flex-wrap: wrap; }
.meta-chips { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.75rem; }
.chip { padding: 0.35rem 0.85rem; border-radius: 999px; background: rgba(102,126,234,0.12); color: #4338ca; font-weight: 700; font-size: 0.85rem; }
.chip.subtle { background: rgba(67,56,202,0.08); color: #312e81; }
.pill { display: inline-flex; padding: 0.25rem 0.65rem; border-radius: 999px; background: rgba(99,102,241,0.1); color: #3730a3; font-weight: 700; font-size: 0.85rem; }
.frosted-table thead { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; }
.frosted-table tbody tr:hover { background: rgba(102,126,234,0.08); }
.ghost { box-shadow: inset 0 0 0 1px rgba(255,255,255,0.4); }

/* Modal Styling */
.large-modal {
  max-width: 90vw !important;
  max-height: 90vh !important;
  width: 100% !important;
  margin: auto !important;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  overflow-y: auto;
  padding: 2rem 1rem;
}

.modal-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 0;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
  transform: scale(1.1);
}

/* Form Styling */
.article-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full {
  grid-column: 1 / -1;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.95rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Editor Container */
.editor-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

:deep(.ql-container) {
  font-size: 1rem;
  border: none;
  min-height: 300px;
}

:deep(.ql-editor) {
  padding: 1rem;
  min-height: 300px;
  max-height: 500px;
  overflow-y: auto;
  color: #333;
}

:deep(.ql-editor.ql-blank::before) {
  color: #999;
  font-style: italic;
}

:deep(.ql-toolbar) {
  border: none;
  border-bottom: 1px solid #ddd;
  background: #f9f9f9;
  padding: 0.75rem;
}

:deep(.ql-toolbar button:hover),
:deep(.ql-toolbar button.ql-active),
:deep(.ql-toolbar.ql-snow .ql-picker-label:hover),
:deep(.ql-toolbar.ql-snow .ql-picker-item:hover),
:deep(.ql-toolbar.ql-snow .ql-picker-item.ql-selected) {
  color: #667eea;
}

/* File Input */
.file-input-group {
  display: flex;
  gap: 0.5rem;
}

.file-input {
  flex: 1;
  padding: 0.75rem;
  border: 2px dashed #ddd;
  border-radius: 8px;
  background: #fafafa;
  cursor: pointer;
  transition: all 0.3s;
}

.file-input:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.file-input-group input[type="text"] {
  flex: 1;
}

.uploading-status {
  color: #667eea;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

/* Responsive */
@media (max-width: 768px) {
  .large-modal {
    max-width: 100% !important;
    border-radius: 12px 12px 0 0;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-overlay {
    padding: 0;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions button {
    width: 100%;
  }
}
</style>
