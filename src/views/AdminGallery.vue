<template>
  <div class="admin-gallery admin-page">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">🎨 مدیریت گالری</div>
        <h2>گالری پروژه‌ها</h2>
        <p class="muted">افزودن و بروزرسانی آیتم‌های گالری و اسلایدر مرتبط</p>
        <div class="meta-chips">
          <span class="chip">{{ items.length }} آیتم</span>
          <span class="chip subtle" v-if="sliders.length">{{ sliders.length }} اسلایدر</span>
        </div>
      </div>
      <div class="header-actions">
        <button @click="showForm = true" class="btn-primary ghost">➕ آیتم جدید</button>
      </div>
    </div>

    <!-- فرم افزودن/ویرایش -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal-card large-modal">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش پروژه' : 'پروژه جدید' }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="submitForm" class="gallery-form">
          <!-- Row 1: Title -->
          <div class="form-group full">
            <label>عنوان پروژه</label>
            <input v-model="formData.title" type="text" placeholder="عنوان جذاب برای پروژه" required />
          </div>

          <!-- Row 2: Category & Duration -->
          <div class="form-row">
            <div class="form-group">
              <label>دسته‌بندی</label>
              <input v-model="formData.category" type="text" placeholder="مثلاً: وب‌سایت" required />
            </div>
            <div class="form-group">
              <label>مدت زمان (اختیاری)</label>
              <input v-model="formData.duration" type="text" placeholder="مثال: 3 ماه" />
            </div>
          </div>

          <!-- Row 3: Description with Quill Editor -->
          <div class="form-group full">
            <label>توضیح خلاصه</label>
            <div class="editor-container">
              <QuillEditor
                v-model:content="formData.description"
                theme="snow"
                content-type="html"
              />
            </div>
          </div>

          <!-- Row 3.5: Full Description with Quill Editor -->
          <div class="form-group full">
            <label>توضیح کامل (برای صفحه جزئیات)</label>
            <div class="editor-container">
              <QuillEditor
                v-model:content="formData.full_description"
                theme="snow"
                content-type="html"
              />
            </div>
          </div>

          <!-- Row 4: Image & Slider -->
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
              <label>گالری (چندین عکس)</label>
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
            <button type="submit" class="btn-primary">{{ editingId ? 'ذخیره تغییرات' : 'ایجاد پروژه' }}</button>
            <button type="button" @click="closeForm" class="btn-secondary">انصراف</button>
          </div>
        </form>
      </div>
    </div>

    <!-- لیست گالری -->
    <div class="gallery-panel">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>در حال بارگذاری پروژه‌ها...</p>
      </div>
      <div v-else-if="items.length === 0" class="empty-state">
        <p>هیچ پروژه‌ای یافت نشد</p>
        <button @click="showForm = true" class="btn-primary">ایجاد اولین پروژه</button>
      </div>
      <div v-else class="card-grid">
        <div v-for="item in items" :key="item.id" class="gallery-card premium-card">
          <div class="card-image-wrapper">
            <img v-if="item.image" :src="item.image" :alt="item.title" class="card-image" />
            <div v-else class="media-placeholder">{{ item.icon || '🎨' }}</div>
            <div class="card-overlay">
              <div class="overlay-badge">{{ item.category }}</div>
            </div>
          </div>
          <div class="card-body">
            <h3 class="card-title">{{ item.title }}</h3>
            <div class="card-meta">
              <span v-if="item.duration" class="meta-item">⏱️ {{ item.duration }}</span>
            </div>
            <div class="card-actions">
              <button @click="editItem(item)" class="btn-edit">✏️ ویرایش</button>
              <button @click="deleteItem(item.id)" class="btn-delete">🗑️ حذف</button>
            </div>
          </div>
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

const items = ref([])
const sliders = ref([])
const loading = ref(false)
const showForm = ref(false)
const editingId = ref(null)
const uploadingImage = ref(false)
const formData = ref({
  title: '',
  description: '',
  full_description: '',
  category: '',
  image: '',
  slider_id: null,
  duration: ''
})

const loadItems = async () => {
  loading.value = true
  try {
    items.value = await adminService.getGalleryItems()
    sliders.value = await adminService.getSliders()
  } catch (error) {
    console.error('Failed to load gallery items:', error)
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در بارگذاری آیتم‌های گالری'); } catch {}
  } finally {
    loading.value = false
  }
}

const editItem = (item) => {
  editingId.value = item.id
  formData.value = { ...item }
  showForm.value = true
}

const submitForm = async () => {
  try {
    if (editingId.value) {
      await adminService.updateGalleryItem(editingId.value, formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('آیتم بروزرسانی شد'); } catch {}
    } else {
      await adminService.createGalleryItem(formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('آیتم ایجاد شد'); } catch {}
    }
    closeForm()
    await loadItems()
  } catch (error) {
    try { const { error: tError } = await import('../composables/useToast.js'); tError(error.response?.data?.detail || 'خطا در ذخیره آیتم'); } catch {}
  }
}

const deleteItem = async (id) => {
  if (!confirm('آیا از حذف این آیتم مطمئن هستید؟')) return
  
  try {
    await adminService.deleteGalleryItem(id)
    try { const { success } = await import('../composables/useToast.js'); success('آیتم حذف شد'); } catch {}
    await loadItems()
  } catch (error) {
    try { const { error: tError } = await import('../composables/useToast.js'); tError(error.response?.data?.detail || 'خطا در حذف آیتم'); } catch {}
  }
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

const closeForm = () => {
  showForm.value = false
  editingId.value = null
  formData.value = {
    title: '',
    description: '',
    full_description: '',
    category: '',
    image: '',
    slider_id: null,
    duration: ''
  }
}

onMounted(() => {
  loadItems()
})
</script>

<style scoped>
/* Layout */
.admin-gallery {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

/* Modal */
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

.large-modal {
  max-width: 700px !important;
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
  color: #333;
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
  transition: all 0.3s;
}

.close-btn:hover {
  color: #333;
  transform: scale(1.1);
}

/* Form Styling */
.gallery-form {
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
  font-weight: 600;
  margin-top: 0.5rem;
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

/* Gallery Panel */
.gallery-panel {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1rem;
  color: #999;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(102, 126, 234, 0.2);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1.5rem;
  color: #999;
  text-align: center;
}

/* Card Grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

.gallery-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.15);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.premium-card {
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.gallery-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.25);
}

.card-image-wrapper {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.gallery-card:hover .card-image {
  transform: scale(1.05);
}

.media-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.gallery-card:hover .card-overlay {
  opacity: 1;
}

.overlay-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.9rem;
  backdrop-filter: blur(10px);
}

/* Card Body */
.card-body {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.75rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.85rem;
  color: #999;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.meta-item {
  display: inline-block;
  background: rgba(102, 126, 234, 0.1);
  padding: 0.3rem 0.7rem;
  border-radius: 8px;
  color: #667eea;
  font-weight: 500;
}

.card-text {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  flex: 1;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.description-html {
  display: block;
}

.description-html :deep(p),
.description-html :deep(li),
.description-html :deep(h1),
.description-html :deep(h2),
.description-html :deep(h3),
.description-html :deep(h4),
.description-html :deep(h5),
.description-html :deep(h6) {
  margin: 0.5rem 0;
  color: #666;
}

.description-html :deep(strong) {
  font-weight: 600;
  color: #333;
}

.description-html :deep(em) {
  font-style: italic;
}

.description-html :deep(ul),
.description-html :deep(ol) {
  padding-right: 1.5rem;
  margin: 0.5rem 0;
}

.description-html :deep(a) {
  color: #667eea;
  text-decoration: none;
}

.description-html :deep(a:hover) {
  text-decoration: underline;
}

/* Card Actions */
.card-actions {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.btn-edit,
.btn-delete {
  flex: 1;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.btn-edit {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.btn-edit:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
}

.btn-delete {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
}

.btn-delete:hover {
  background: rgba(220, 38, 38, 0.2);
  transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-overlay {
    padding: 0;
  }

  .modal-card {
    border-radius: 12px 12px 0 0;
    max-height: 100%;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions button {
    width: 100%;
  }

  .large-modal {
    max-width: 100% !important;
  }
}
</style>
