<template>
  <div class="admin-sliders">
    <div class="header-actions">
      <button @click="showForm = true" class="btn-primary">
        ➕ اسلایدر جدید
      </button>
    </div>

    <!-- فرم افزودن/ویرایش -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal-card">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش اسلایدر' : 'اسلایدر جدید' }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="submitForm" class="slider-form">
          <div class="form-group">
            <label>نام اسلایدر</label>
            <input v-model="formData.name" type="text" required />
          </div>

          <div class="form-group">
            <label>توضیح (اختیاری)</label>
            <textarea v-model="formData.description" rows="2"></textarea>
          </div>

          <div class="form-group">
            <label>تصاویر در اسلایدر</label>
            <div class="images-manager">
              <div class="add-images">
                <div class="file-input-wrapper">
                  <input 
                    type="file" 
                    @change="handleImageUpload" 
                    accept="image/*"
                    class="file-input"
                    multiple
                  />
                  <span class="upload-label">📁 انتخاب تصاویر</span>
                </div>
                <div class="url-input">
                  <input v-model="newImageUrl" type="url" placeholder="یا URL تصویر را پیوند کنید" />
                  <button type="button" @click="addImageUrl" class="btn-small">اضافه کنید</button>
                </div>
                <div v-if="uploadingImage" class="uploading-status">درحال آپلود...</div>
              </div>

              <div class="images-preview">
                <h4>تصاویر انتخاب‌شده ({{ formData.images.length }})</h4>
                <div v-if="formData.images.length === 0" class="no-images">
                  هنوز تصویری اضافه نشده است
                </div>
                <div v-else class="images-list">
                  <div v-for="(image, index) in formData.images" :key="index" class="image-item">
                    <img :src="image" :alt="`Image ${index + 1}`" />
                    <button type="button" @click="removeImage(index)" class="btn-remove">✕</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ editingId ? 'ذخیره تغییرات' : 'ایجاد اسلایدر' }}</button>
            <button type="button" @click="closeForm" class="btn-secondary">انصراف</button>
          </div>
        </form>
      </div>
    </div>

    <!-- لیست اسلایدرها -->
    <div class="sliders-list">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="sliders.length === 0" class="empty">
        <p>هیچ اسلایدری یافت نشد</p>
      </div>
      <div v-else class="sliders-grid">
        <div v-for="slider in sliders" :key="slider.id" class="slider-card">
          <div class="card-preview">
            <div v-if="slider.images && slider.images.length > 0" class="preview-images">
              <img 
                v-for="(image, idx) in slider.images.slice(0, 3)" 
                :key="idx" 
                :src="image" 
                :alt="`Image ${idx + 1}`" 
                class="preview-img"
              />
              <div v-if="slider.images.length > 3" class="more-count">
                +{{ slider.images.length - 3 }}
              </div>
            </div>
            <div v-else class="no-preview">
              🖼️ بدون تصویر
            </div>
          </div>
          <div class="card-content">
            <h3>{{ slider.name }}</h3>
            <p v-if="slider.description" class="description">{{ slider.description }}</p>
            <div class="images-count">
              📷 {{ slider.images ? slider.images.length : 0 }} تصویر
            </div>
          </div>
          <div class="card-actions">
            <button @click="editSlider(slider)" class="btn-edit">✏️ ویرایش</button>
            <button @click="deleteSlider(slider.id)" class="btn-delete">🗑️ حذف</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminService } from '../api/services'

const sliders = ref([])
const loading = ref(false)
const showForm = ref(false)
const editingId = ref(null)
const uploadingImage = ref(false)
const newImageUrl = ref('')
const formData = ref({
  name: '',
  description: '',
  images: []
})

const loadSliders = async () => {
  loading.value = true
  try {
    sliders.value = await adminService.getSliders()
  } catch (error) {
    console.error('Failed to load sliders:', error)
    alert('خطا در بارگذاری اسلایدرها')
  } finally {
    loading.value = false
  }
}

const editSlider = (slider) => {
  editingId.value = slider.id
  formData.value = { ...slider }
  showForm.value = true
}

const submitForm = async () => {
  try {
    if (editingId.value) {
      await adminService.updateSlider(editingId.value, formData.value)
      alert('اسلایدر با موفقیت به‌روزرسانی شد')
    } else {
      await adminService.createSlider(formData.value)
      alert('اسلایدر با موفقیت ایجاد شد')
    }
    closeForm()
    await loadSliders()
  } catch (error) {
    alert('خطا: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  }
}

const deleteSlider = async (id) => {
  if (!confirm('آیا از حذف این اسلایدر مطمئن هستید؟')) return
  
  try {
    await adminService.deleteSlider(id)
    alert('اسلایدر با موفقیت حذف شد')
    await loadSliders()
  } catch (error) {
    alert('خطا: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  }
}

const addImageUrl = () => {
  if (newImageUrl.value.trim()) {
    if (!formData.value.images) {
      formData.value.images = []
    }
    formData.value.images.push(newImageUrl.value)
    newImageUrl.value = ''
  }
}

const removeImage = (index) => {
  formData.value.images.splice(index, 1)
}

const closeForm = () => {
  showForm.value = false
  editingId.value = null
  newImageUrl.value = ''
  formData.value = {
    name: '',
    description: '',
    images: []
  }
}

const handleImageUpload = async (event) => {
  const files = event.target.files
  if (files.length === 0) return

  uploadingImage.value = true
  try {
    if (!formData.value.images) {
      formData.value.images = []
    }
    
    for (let file of files) {
      const formDataFile = new FormData()
      formDataFile.append('file', file)
      const response = await adminService.uploadFile(formDataFile)
      formData.value.images.push(response.url)
    }
  } catch (error) {
    alert('خطا در آپلود تصویر: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  } finally {
    uploadingImage.value = false
  }
}

onMounted(() => {
  loadSliders()
})
</script>

<style scoped>
.admin-sliders {
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
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
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
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #718096;
  transition: all 0.3s;
}

.close-btn:hover {
  color: #2d3748;
}

.slider-form {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
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
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.95rem;
  color: #2d3748;
  transition: all 0.3s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.images-manager {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  background: #f7fafc;
}

.add-images {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.file-input-wrapper {
  position: relative;
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.upload-label {
  display: block;
  padding: 1rem;
  border: 2px dashed #667eea;
  border-radius: 6px;
  cursor: pointer;
  background: white;
  text-align: center;
  font-weight: 600;
  color: #667eea;
  transition: all 0.3s;
}

.upload-label:hover {
  background: #edf2f7;
  border-color: #764ba2;
}

.url-input {
  display: flex;
  gap: 0.5rem;
}

.url-input input {
  flex: 1;
}

.btn-small {
  padding: 0.75rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-small:hover {
  background: #764ba2;
}

.uploading-status {
  color: #667eea;
  font-size: 0.85rem;
  font-weight: 500;
}

.images-preview {
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
}

.images-preview h4 {
  margin: 0 0 1rem 0;
  color: #2d3748;
}

.no-images {
  text-align: center;
  color: #a0aec0;
  padding: 1rem;
}

.images-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 0.75rem;
}

.image-item {
  position: relative;
  border-radius: 6px;
  overflow: hidden;
  aspect-ratio: 1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.btn-remove {
  position: absolute;
  top: -1px;
  right: -1px;
  background: #e53e3e;
  color: white;
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 0;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  opacity: 0;
}

.image-item:hover .btn-remove {
  opacity: 1;
}

.btn-remove:hover {
  background: #c53030;
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

.sliders-list {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.loading,
.empty {
  text-align: center;
  color: #718096;
  padding: 2rem;
}

.sliders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.slider-card {
  background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.slider-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.card-preview {
  width: 100%;
  height: 160px;
  background: linear-gradient(135deg, #f7fafc 0%, #e2e8f0 100%);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  overflow: hidden;
  position: relative;
}

.preview-images {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 1fr;
  gap: 1px;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.more-count {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.no-preview {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #a0aec0;
}

.card-content {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.card-content h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #2d3748;
  font-weight: 600;
}

.description {
  margin: 0;
  font-size: 0.85rem;
  color: #718096;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.images-count {
  display: inline-block;
  width: fit-content;
  padding: 0.35rem 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
  margin-top: auto;
}

.btn-edit,
.btn-delete {
  flex: 1;
  padding: 0.6rem 0.75rem;
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.3s;
  font-weight: 600;
  white-space: nowrap;
}

.btn-edit:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  color: white;
}

.btn-delete:hover {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-color: #f5576c;
  color: white;
}

@media (max-width: 768px) {
  .sliders-grid {
    grid-template-columns: 1fr;
  }

  .modal-card {
    max-width: 90%;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
