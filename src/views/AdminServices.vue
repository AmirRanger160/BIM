<template>
  <div class="admin-services admin-page">
    <div class="section-header">
      <h2>مدیریت خدمات</h2>
      <button @click="openAddDialog" class="btn-add">+ افزودن خدمت</button>
    </div>

    <div v-if="loading" class="loading">در حال بارگذاری...</div>

    <div v-else class="services-table table-card">
      <table>
        <thead>
          <tr>
            <th>شناسه</th>
            <th>عنوان</th>
            <th>آیکون</th>
            <th>قیمت</th>
            <th>ترتیب</th>
            <th>وضعیت</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.id">
            <td>{{ service.id }}</td>
            <td>{{ service.title }}</td>
            <td><span class="service-icon">{{ service.icon }}</span></td>
            <td>{{ service.price || '-' }}</td>
            <td>{{ service.order }}</td>
            <td>
              <span :class="['status-badge', service.active ? 'active' : 'inactive']">
                {{ service.active ? 'فعال' : 'غیرفعال' }}
              </span>
            </td>
            <td class="actions">
              <button @click="editService(service)" class="btn-edit">ویرایش</button>
              <button @click="deleteService(service.id)" class="btn-delete">حذف</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Dialog -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showDialog" class="modal-overlay" @click="closeDialog">
          <div class="modal-dialog" @click.stop>
            <h3>{{ editingId ? 'ویرایش خدمت' : 'افزودن خدمت جدید' }}</h3>
            
            <form @submit.prevent="saveService">
              <div class="form-row">
                <div class="form-group">
                  <label for="service-title">عنوان خدمت*</label>
                  <input
                    id="service-title"
                    v-model="formData.title"
                    type="text"
                    required
                    placeholder="مثلاً: طراحی وب"
                  />
                </div>

                <div class="form-group">
                  <label for="service-icon">آیکون</label>
                  <input
                    id="service-icon"
                    v-model="formData.icon"
                    type="text"
                    placeholder="🎯"
                  />
                </div>
              </div>

              <div class="form-group">
                <label for="service-description">توضیحات*</label>
                <textarea
                  id="service-description"
                  v-model="formData.description"
                  rows="3"
                  required
                  placeholder="توضیحات کامل خدمت"
                ></textarea>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="service-color">رنگ</label>
                  <input
                    id="service-color"
                    v-model="formData.color"
                    type="text"
                    placeholder="#667eea"
                  />
                </div>

                <div class="form-group">
                  <label for="service-price">قیمت</label>
                  <input
                    id="service-price"
                    v-model="formData.price"
                    type="text"
                    placeholder="از 10 میلیون تومان"
                  />
                </div>
              </div>

              <div class="form-group">
                <label for="service-gradient">گرادیانت (CSS)</label>
                <input
                  id="service-gradient"
                  v-model="formData.gradient"
                  type="text"
                  placeholder="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                />
              </div>

              <div class="form-group">
                <label for="service-image">تصویر شاخص</label>
                <div class="image-upload-group">
                  <input
                    type="file"
                    accept="image/*"
                    @change="handleImageUpload"
                    :disabled="uploading"
                    class="file-input"
                  />
                  <div v-if="uploading" class="upload-status">در حال آپلود...</div>
                  <div v-if="formData.image" class="image-preview">
                    <img :src="formData.image" alt="پیش‌نمایش" />
                    <button type="button" @click="formData.image = ''" class="btn-remove-image">×</button>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label for="service-slider">اسلایدر</label>
                <select id="service-slider" v-model.number="formData.slider_id">
                  <option :value="null">بدون اسلایدر</option>
                  <option v-for="slider in sliders" :key="slider.id" :value="slider.id">
                    {{ slider.name }} ({{ slider.images?.length || 0 }} تصویر)
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label for="service-features">ویژگی‌ها (هر خط یک ویژگی)</label>
                <textarea
                  id="service-features"
                  v-model="featuresText"
                  rows="4"
                  placeholder="طراحی UI/UX حرفه‌ای&#10;ریسپانسیو و موبایل فرندلی&#10;بهینه‌سازی SEO"
                ></textarea>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="service-order">ترتیب نمایش</label>
                  <input
                    id="service-order"
                    v-model.number="formData.order"
                    type="number"
                    min="0"
                  />
                </div>

                <div class="form-group">
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="formData.active" />
                    <span>فعال</span>
                  </label>
                </div>
              </div>

              <div class="form-actions">
                <button type="button" @click="closeDialog" class="btn-cancel">
                  انصراف
                </button>
                <button type="submit" class="btn-submit">
                  {{ editingId ? 'بروزرسانی' : 'افزودن' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Confirmation Dialog -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showConfirm" class="modal-overlay" @click="showConfirm = false">
          <div class="confirm-dialog" @click.stop>
            <p>آیا از حذف این خدمت اطمینان دارید؟</p>
            <div class="confirm-actions">
              <button @click="showConfirm = false" class="btn-cancel">انصراف</button>
              <button @click="confirmDelete" class="btn-delete">حذف</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminService } from '../api/services'

const services = ref([])
const sliders = ref([])
const loading = ref(true)
const uploading = ref(false)
const showDialog = ref(false)
const showConfirm = ref(false)
const editingId = ref(null)
const deleteTargetId = ref(null)

const formData = ref({
  title: '',
  description: '',
  icon: '🎯',
  color: '#667eea',
  gradient: '',
  image: '',
  slider_id: null,
  features: [],
  price: '',
  order: 0,
  active: true
})

const featuresText = computed({
  get: () => formData.value.features.join('\n'),
  set: (value) => {
    formData.value.features = value
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0)
  }
})

const resetForm = () => {
  formData.value = {
    title: '',
    description: '',
    icon: '🎯',
    color: '#667eea',
    gradient: '',
    image: '',
    slider_id: null,
    features: [],
    price: '',
    order: 0,
    active: true
  }
}

const openAddDialog = () => {
  editingId.value = null
  resetForm()
  showDialog.value = true
}

const editService = (service) => {
  editingId.value = service.id
  formData.value = {
    title: service.title,
    description: service.description || '',
    icon: service.icon || '🎯',
    color: service.color || '#667eea',
    gradient: service.gradient || '',
    image: service.image || '',
    slider_id: service.slider_id || null,
    features: service.features || [],
    price: service.price || '',
    order: service.order || 0,
    active: service.active !== false
  }
  showDialog.value = true
}

const closeDialog = () => {
  showDialog.value = false
  editingId.value = null
  resetForm()
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  try {
    uploading.value = true
    const formData_ = new FormData()
    formData_.append('file', file)
    const response = await adminService.uploadFile(formData_)
    // Handle different response formats
    formData.value.image = response.url || response.data?.url || response
  } catch (error) {
    console.error('خطا در آپلود تصویر:', error)
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در آپلود تصویر'); } catch {}
  } finally {
    uploading.value = false
  }
}

const saveService = async () => {
  try {
    if (editingId.value) {
      await adminService.updateService(editingId.value, formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('خدمت بروزرسانی شد'); } catch {}
    } else {
      await adminService.createService(formData.value)
      try { const { success } = await import('../composables/useToast.js'); success('خدمت با موفقیت اضافه شد'); } catch {}
    }
    
    await fetchServices()
    closeDialog()
  } catch (error) {
    console.error('خطا در ذخیره خدمت:', error)
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در ذخیره خدمت'); } catch {}
  }
}

const deleteService = (id) => {
  deleteTargetId.value = id
  showConfirm.value = true
}

const confirmDelete = async () => {
  try {
    await adminService.deleteService(deleteTargetId.value)
    try { const { success } = await import('../composables/useToast.js'); success('خدمت حذف شد'); } catch {}
    await fetchServices()
    showConfirm.value = false
    deleteTargetId.value = null
  } catch (error) {
    console.error('خطا در حذف خدمت:', error)
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در حذف خدمت'); } catch {}
  }
}

const fetchServices = async () => {
  try {
    loading.value = true
    const response = await adminService.getServices()
    services.value = Array.isArray(response) ? response : response.data || []
  } catch (error) {
    console.error('خطا در دریافت خدمات:', error)
    services.value = []
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در دریافت خدمات'); } catch {}
  } finally {
    loading.value = false
  }
}

const fetchSliders = async () => {
  try {
    const response = await adminService.getSliders()
    sliders.value = Array.isArray(response) ? response : response.data || []
  } catch (error) {
    console.error('خطا در دریافت اسلایدرها:', error)
    sliders.value = []
    try { const { error: tError } = await import('../composables/useToast.js'); tError('خطا در دریافت اسلایدرها'); } catch {}
  }
}

onMounted(() => {
  fetchServices()
  fetchSliders()
})
</script>

<style scoped>
/* This view now uses the global admin theme (admin.css). */
.service-icon { font-size: 1.5rem; }
</style>
