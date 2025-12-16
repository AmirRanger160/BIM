<template>
  <div class="admin-page admin-videos">
    <div class="admin-section-header">
      <div>
        <div class="eyebrow">🎬 ویدیوها</div>
        <h2>مدیریت ویدیوهای نمایشی</h2>
        <p class="muted">اضافه کردن و ویرایش ویدیوهای صفحه اصلی</p>
      </div>
      <div class="header-actions">
        <button @click="showForm = true" class="btn-primary">➕ ویدیوی جدید</button>
      </div>
    </div>

    <!-- فرم ایجاد/ویرایش -->
    <div v-if="showForm" class="panel form-panel">
      <div class="panel-header">
        <h3>{{ editingVideo ? 'ویرایش ویدیو' : 'ویدیوی جدید' }}</h3>
        <button @click="showForm = false" class="btn-close">✕</button>
      </div>

      <form @submit.prevent="saveVideo" class="form-grid">
        <div class="form-group">
          <label>عنوان</label>
          <input
            v-model="formData.title"
            type="text"
            required
            placeholder="عنوان ویدیو"
          />
        </div>

        <div class="form-group">
          <label>توضیح</label>
          <textarea
            v-model="formData.description"
            placeholder="توضیح کوتاه ویدیو"
            rows="3"
          ></textarea>
        </div>

        <div class="form-group full-width">
          <label>لینک ویدیو</label>
          <input
            v-model="formData.video_url"
            type="url"
            required
            placeholder="https://www.youtube.com/embed/... یا لینک درخواست"
          />
          <small class="hint">لینک YouTube یا Vimeo یا هر سایت دیگر</small>
        </div>

        <div class="form-group">
          <label>تصویر بند انگشتی (اختیاری)</label>
          <input
            v-model="formData.thumbnail"
            type="url"
            placeholder="https://..."
          />
        </div>

        <div class="form-group">
          <label>مدت زمان (اختیاری)</label>
          <input
            v-model="formData.duration"
            type="text"
            placeholder="مثال: 5:30"
          />
        </div>

        <div class="form-group">
          <label>ترتیب نمایش</label>
          <input
            v-model.number="formData.order"
            type="number"
            min="0"
          />
        </div>

        <div class="form-group">
          <label>
            <input v-model="formData.active" type="checkbox" />
            فعال
          </label>
        </div>

        <div class="form-actions full-width">
          <button type="submit" class="btn-primary">{{ editingVideo ? 'بروزرسانی' : 'ایجاد' }}</button>
          <button type="button" @click="resetForm" class="btn-secondary">انصراف</button>
        </div>
      </form>
    </div>

    <!-- لیست ویدیوها -->
    <div class="panel videos-panel">
      <div class="panel-header">
        <h3>ویدیوهای موجود</h3>
        <span class="muted">تعداد: {{ videos.length }}</span>
      </div>

      <div v-if="videos.length === 0" class="empty-state">
        <p>هیچ ویدیویی وجود ندارد</p>
        <button @click="showForm = true" class="btn-primary">ایجاد ویدیو اول</button>
      </div>

      <div v-else class="videos-grid">
        <div v-for="video in videos" :key="video.id" class="video-card">
          <div class="video-preview">
            <img
              v-if="video.thumbnail"
              :src="video.thumbnail"
              :alt="video.title"
              class="thumbnail"
            />
            <div v-else class="no-thumbnail">
              <span class="icon">🎬</span>
            </div>
            <div class="video-duration" v-if="video.duration">
              {{ video.duration }}
            </div>
          </div>

          <div class="video-info">
            <h4>{{ video.title }}</h4>
            <p class="description">{{ video.description }}</p>
            <div class="video-meta">
              <span class="badge" :class="{ active: video.active }">
                {{ video.active ? '✓ فعال' : '✗ غیرفعال' }}
              </span>
              <span class="views">👁️ {{ video.views }}</span>
            </div>
          </div>

          <div class="video-actions">
            <button
              @click="editVideo(video)"
              class="btn-small btn-primary"
              title="ویرایش"
            >
              ✎
            </button>
            <button
              @click="toggleVideo(video)"
              class="btn-small"
              :class="video.active ? 'btn-warning' : 'btn-success'"
              :title="video.active ? 'غیرفعال کردن' : 'فعال کردن'"
            >
              {{ video.active ? '○' : '●' }}
            </button>
            <button
              @click="deleteVideo(video)"
              class="btn-small btn-danger"
              title="حذف"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminService } from '../api/services'
import { success, error } from '../composables/useToast'

const showToast = (message, type) => {
  if (type === 'success') {
    success(message)
  } else if (type === 'error') {
    error(message)
  }
}

const videos = ref([])
const showForm = ref(false)
const editingVideo = ref(null)

const formData = ref({
  title: '',
  description: '',
  video_url: '',
  thumbnail: '',
  duration: '',
  active: true,
  order: 0
})

onMounted(async () => {
  await loadVideos()
})

const loadVideos = async () => {
  try {
    const response = await fetch('/api/videos?active_only=false&limit=100')
    if (!response.ok) throw new Error('خطا در بارگذاری ویدیوها')
    videos.value = await response.json()
  } catch (error) {
    console.error('خطا:', error)
    showToast('خطا در بارگذاری ویدیوها', 'error')
  }
}

const saveVideo = async () => {
  try {
    const url = editingVideo.value
      ? `/api/videos/${editingVideo.value.id}`
      : '/api/videos'
    
    const method = editingVideo.value ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })

    if (!response.ok) throw new Error('خطا در ذخیره')
    
    await loadVideos()
    resetForm()
    showToast(
      editingVideo.value ? 'ویدیو بروزرسانی شد' : 'ویدیو ایجاد شد',
      'success'
    )
  } catch (error) {
    console.error('خطا:', error)
    showToast('خطا در ذخیره ویدیو', 'error')
  }
}

const editVideo = (video) => {
  editingVideo.value = video
  formData.value = { ...video }
  showForm.value = true
}

const resetForm = () => {
  editingVideo.value = null
  formData.value = {
    title: '',
    description: '',
    video_url: '',
    thumbnail: '',
    duration: '',
    active: true,
    order: 0
  }
  showForm.value = false
}

const toggleVideo = async (video) => {
  try {
    const response = await fetch(`/api/videos/${video.id}/toggle`, {
      method: 'POST'
    })
    if (!response.ok) throw new Error('خطا')
    
    await loadVideos()
    showToast('وضعیت ویدیو تغییر کرد', 'success')
  } catch (error) {
    console.error('خطا:', error)
    showToast('خطا در تغییر وضعیت', 'error')
  }
}

const deleteVideo = async (video) => {
  if (!confirm(`آیا مطمئن هستید؟\n${video.title}`)) return

  try {
    const response = await fetch(`/api/videos/${video.id}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('خطا')
    
    await loadVideos()
    showToast('ویدیو حذف شد', 'success')
  } catch (error) {
    console.error('خطا:', error)
    showToast('خطا در حذف ویدیو', 'error')
  }
}
</script>

<style scoped>
.admin-videos {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-panel {
  margin-top: 1rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.95rem;
}

.dark-mode .form-group label {
  color: #d1d5db;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-family: inherit;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.dark-mode .form-group input,
.dark-mode .form-group textarea {
  border-color: #4b5563;
  background: #1f2937;
  color: #f3f4f6;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group .hint {
  font-size: 0.85rem;
  color: #6b7280;
}

.dark-mode .form-group .hint {
  color: #9ca3af;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.dark-mode .form-actions {
  border-top-color: #4b5563;
}

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.video-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.dark-mode .video-card {
  background: #111827;
  border-color: #374151;
}

.video-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.video-preview {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: #e5e7eb;
}

.dark-mode .video-preview {
  background: #1f2937;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-thumbnail {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-size: 3rem;
}

.video-duration {
  position: absolute;
  bottom: 0.5rem;
  left: 0.5rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.video-info {
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.video-info h4 {
  margin: 0;
  font-size: 1rem;
  color: #1f2937;
  line-height: 1.4;
  word-break: break-word;
}

.dark-mode .video-info h4 {
  color: #f3f4f6;
}

.description {
  margin: 0;
  color: #6b7280;
  font-size: 0.85rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.dark-mode .description {
  color: #9ca3af;
}

.video-meta {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  background: #fecaca;
  color: #7f1d1d;
}

.badge.active {
  background: #bbf7d0;
  color: #166534;
}

.views {
  font-size: 0.85rem;
  color: #6b7280;
}

.dark-mode .views {
  color: #9ca3af;
}

.video-actions {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.dark-mode .video-actions {
  border-top-color: #374151;
}

.btn-small {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 600;
}

.btn-small.btn-primary {
  background: #667eea;
  color: white;
}

.btn-small.btn-primary:hover {
  background: #5568d3;
}

.btn-small.btn-success {
  background: #10b981;
  color: white;
}

.btn-small.btn-success:hover {
  background: #059669;
}

.btn-small.btn-warning {
  background: #f59e0b;
  color: white;
}

.btn-small.btn-warning:hover {
  background: #d97706;
}

.btn-small.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-small.btn-danger:hover {
  background: #dc2626;
}

.empty-state {
  padding: 3rem 1.5rem;
  text-align: center;
  color: #6b7280;
}

.dark-mode .empty-state {
  color: #9ca3af;
}

.empty-state p {
  margin: 0 0 1rem;
  font-size: 1.1rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  transition: color 0.2s ease;
}

.btn-close:hover {
  color: #1f2937;
}

.dark-mode .btn-close {
  color: #9ca3af;
}

.dark-mode .btn-close:hover {
  color: #f3f4f6;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .videos-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
