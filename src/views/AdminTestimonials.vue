<template>
  <div class="admin-testimonials">
    <div class="header-actions">
      <button @click="showForm = true" class="btn-primary">
        ➕ نظر جدید
      </button>
    </div>

    <!-- فرم افزودن/ویرایش -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal-card">
        <div class="modal-header">
          <h2>{{ editingId ? 'ویرایش نظر' : 'نظر جدید' }}</h2>
          <button @click="closeForm" class="close-btn">✕</button>
        </div>
        <form @submit.prevent="submitForm" class="testimonial-form">
          <div class="form-row">
            <div class="form-group">
              <label>نام</label>
              <input v-model="formData.name" type="text" required />
            </div>
            <div class="form-group">
              <label>عنوان/شغل</label>
              <input v-model="formData.role" type="text" required />
            </div>
          </div>

          <div class="form-group">
            <label>نظر</label>
            <textarea v-model="formData.text" rows="4" required></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>امتیاز (1-5)</label>
              <input v-model.number="formData.rating" type="number" min="1" max="5" />
            </div>
            <div class="form-group">
              <label>پروژه</label>
              <input v-model="formData.project" type="text" />
            </div>
          </div>

          <div class="form-group">
            <label>تصویر پروفایل (URL یا آپلود)</label>
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

          <div class="form-actions">
            <button type="submit" class="btn-primary">{{ editingId ? 'ذخیره تغییرات' : 'ایجاد نظر' }}</button>
            <button type="button" @click="closeForm" class="btn-secondary">انصراف</button>
          </div>
        </form>
      </div>
    </div>

    <!-- لیست نظرات -->
    <div class="testimonials-list">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="testimonials.length === 0" class="empty">
        <p>هیچ نظری یافت نشد</p>
      </div>
      <div v-else>
        <div class="testimonials-container">
          <div v-for="testimonial in testimonials" :key="testimonial.id" class="testimonial-card" :class="{ pending: !testimonial.approved }">
            <div class="testimonial-header">
              <div class="user-info">
                <div class="avatar">{{ testimonial.avatar || '👤' }}</div>
                <div class="info">
                  <h3>{{ testimonial.name }}</h3>
                  <p>{{ testimonial.role }}</p>
                </div>
              </div>
              <div class="rating">
                <span v-for="i in testimonial.rating" :key="i">⭐</span>
              </div>
            </div>

            <div class="testimonial-text">
              {{ testimonial.text }}
            </div>

            <div v-if="testimonial.project" class="project-tag">
              {{ testimonial.project }}
            </div>

            <div class="testimonial-actions">
              <button 
                v-if="!testimonial.approved"
                @click="approveTestimonial(testimonial.id)"
                class="btn-approve"
              >
                ✓ تایید
              </button>
              <span v-else class="approved-badge">✓ تایید شده</span>
              <button @click="editTestimonial(testimonial)" class="btn-edit">✏️</button>
              <button @click="deleteTestimonial(testimonial.id)" class="btn-delete">🗑️</button>
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

const testimonials = ref([])
const loading = ref(false)
const showForm = ref(false)
const editingId = ref(null)
const uploadingImage = ref(false)
const formData = ref({
  name: '',
  role: '',
  text: '',
  rating: 5,
  project: '',
  image: '',
  avatar: '👤'
})

const loadTestimonials = async () => {
  loading.value = true
  try {
    testimonials.value = await adminService.getTestimonials()
  } catch (error) {
    console.error('Failed to load testimonials:', error)
    alert('خطا در بارگذاری نظرات')
  } finally {
    loading.value = false
  }
}

const editTestimonial = (testimonial) => {
  editingId.value = testimonial.id
  formData.value = { ...testimonial }
  showForm.value = true
}

const submitForm = async () => {
  try {
    if (editingId.value) {
      await adminService.updateTestimonial(editingId.value, formData.value)
      alert('نظر با موفقیت به‌روزرسانی شد')
    } else {
      await adminService.createTestimonial(formData.value)
      alert('نظر با موفقیت ایجاد شد')
    }
    closeForm()
    await loadTestimonials()
  } catch (error) {
    alert('خطا: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  }
}

const approveTestimonial = async (id) => {
  try {
    await adminService.approveTestimonial(id)
    alert('نظر تایید شد')
    await loadTestimonials()
  } catch (error) {
    alert('خطا: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  }
}

const deleteTestimonial = async (id) => {
  if (!confirm('آیا از حذف این نظر مطمئن هستید؟')) return
  
  try {
    await adminService.deleteTestimonial(id)
    alert('نظر با موفقیت حذف شد')
    await loadTestimonials()
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
    name: '',
    role: '',
    text: '',
    rating: 5,
    project: '',
    image: '',
    avatar: '👤'
  }
}

onMounted(() => {
  loadTestimonials()
})
</script>

<style scoped>
.admin-testimonials {
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

.testimonial-form {
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
  color: #2d3748;
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

.testimonials-list {
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

.testimonials-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.testimonial-card {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  background: white;
  transition: all 0.3s;
}

.testimonial-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.testimonial-card.pending {
  background: #fffaf0;
  border-color: #fbd38d;
}

.testimonial-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.user-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.avatar {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7fafc;
  border-radius: 50%;
}

.info h3 {
  margin: 0;
  color: #2d3748;
  font-size: 1rem;
}

.info p {
  margin: 0.25rem 0 0 0;
  color: #718096;
  font-size: 0.9rem;
}

.rating {
  display: flex;
  gap: 0.25rem;
}

.testimonial-text {
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.project-tag {
  display: inline-block;
  background: #edf2f7;
  color: #667eea;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}

.testimonial-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-approve,
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

.btn-approve {
  background: #c6f6d5;
  border-color: #9ae6b4;
  color: #22543d;
}

.btn-approve:hover {
  background: #9ae6b4;
}

.btn-edit:hover {
  background: #edf2f7;
  border-color: #667eea;
}

.btn-delete:hover {
  background: #fff5f5;
  border-color: #e53e3e;
}

.approved-badge {
  color: #22863a;
  background: #f0f8f4;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-card {
    width: 95%;
  }

  .testimonial-header {
    flex-direction: column;
    gap: 1rem;
  }

  .testimonial-actions {
    flex-wrap: wrap;
  }
}
</style>
