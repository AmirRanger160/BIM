<template>
  <div class="admin-gallery">
    <div class="header-actions">
      <button @click="showForm = true" class="btn-primary">
        ➕ آیتم جدید
      </button>
    </div>

    <!-- فرم افزودن/ویرایش -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal-card">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش آیتم' : 'آیتم جدید' }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="submitForm" class="gallery-form">
          <div class="form-row">
            <div class="form-group">
              <label>عنوان</label>
              <input v-model="formData.title" type="text" required />
            </div>
            <div class="form-group">
              <label>دسته‌بندی</label>
              <input v-model="formData.category" type="text" required />
            </div>
          </div>

          <div class="form-group">
            <label>توضیح</label>
            <textarea v-model="formData.description" rows="3" required></textarea>
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

          <div class="form-row">
            <div class="form-group">
              <label>اسلایدر (چندین عکس)</label>
              <select v-model="formData.slider_id">
                <option :value="null">-- انتخاب نکنید --</option>
                <option v-for="slider in sliders" :key="slider.id" :value="slider.id">
                  {{ slider.name }} ({{ slider.images?.length || 0 }} عکس)
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>مدت زمان</label>
              <input v-model="formData.duration" type="text" placeholder="مثال: 2 ساعت" />
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ editingId ? 'ذخیره تغییرات' : 'ایجاد آیتم' }}</button>
            <button type="button" @click="closeForm" class="btn-secondary">انصراف</button>
          </div>
        </form>
      </div>
    </div>

    <!-- لیست گالری -->
    <div class="gallery-list">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="items.length === 0" class="empty">
        <p>هیچ آیتمی یافت نشد</p>
      </div>
      <div v-else class="gallery-grid">
        <div v-for="item in items" :key="item.id" class="gallery-card">
          <div class="card-image">
            <img v-if="item.image" :src="item.image" :alt="item.title" />
            <div v-else class="no-image">{{ item.icon || '🎨' }}</div>
          </div>
          <div class="card-content">
            <h3>{{ item.title }}</h3>
            <p class="category">{{ item.category }}</p>
            <p class="description">{{ item.description }}</p>
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
    alert('خطا در بارگذاری آیتم‌های گالری')
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
      alert('آیتم با موفقیت به‌روزرسانی شد')
    } else {
      await adminService.createGalleryItem(formData.value)
      alert('آیتم با موفقیت ایجاد شد')
    }
    closeForm()
    await loadItems()
  } catch (error) {
    alert('خطا: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  }
}

const deleteItem = async (id) => {
  if (!confirm('آیا از حذف این آیتم مطمئن هستید؟')) return
  
  try {
    await adminService.deleteGalleryItem(id)
    alert('آیتم با موفقیت حذف شد')
    await loadItems()
  } catch (error) {
    alert('خطا: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
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
    alert('خطا در آپلود تصویر: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
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
.admin-gallery {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
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
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-card {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
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

.gallery-form {
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
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.95rem;
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

.gallery-list {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 2rem;
}

.loading,
.empty {
  text-align: center;
  color: #718096;
  padding: 2rem;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.gallery-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: all 0.3s;
}

.gallery-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.card-image {
  width: 100%;
  height: 200px;
  background: #f7fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  font-size: 3rem;
}

.card-content {
  padding: 1rem;
}

.card-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #2d3748;
}

.category {
  margin: 0;
  font-size: 0.85rem;
  color: #667eea;
  font-weight: 600;
}

.description {
  margin: 0.5rem 0;
  font-size: 0.85rem;
  color: #718096;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-edit,
.btn-delete {
  flex: 1;
  padding: 0.5rem;
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

  .gallery-grid {
    grid-template-columns: 1fr;
  }
}
</style>
