<template>
  <div class="admin-contacts">
    <div class="header-info">
      <div class="info-card">
        <span class="label">کل پیام‌ها</span>
        <span class="value">{{ contacts.length }}</span>
      </div>
      <div class="info-card alert">
        <span class="label">خوانده‌نشده</span>
        <span class="value">{{ unreadCount }}</span>
      </div>
    </div>

    <!-- لیست پیام‌ها -->
    <div class="contacts-list">
      <div v-if="loading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="contacts.length === 0" class="empty">
        <p>هیچ پیامی یافت نشد</p>
      </div>
      <div v-else>
        <div class="contacts-container">
          <div 
            v-for="contact in contacts" 
            :key="contact.id" 
            class="contact-card"
            :class="{ unread: !contact.read }"
            @click="selectedContact = contact"
          >
            <div class="contact-header">
              <div class="contact-name">{{ contact.name }}</div>
              <div v-if="!contact.read" class="unread-badge">جدید</div>
            </div>
            <div class="contact-email">{{ contact.email }}</div>
            <div class="contact-subject">{{ contact.subject }}</div>
            <div class="contact-date">{{ formatDate(contact.created_at) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- جزئیات پیام -->
    <div v-if="selectedContact" class="modal-overlay" @click.self="selectedContact = null">
      <div class="modal-card">
        <div class="modal-header">
          <h2>{{ selectedContact.subject }}</h2>
          <button @click="selectedContact = null" class="close-btn">✕</button>
        </div>
        <div class="contact-details">
          <div class="detail-section">
            <h3>از طرف:</h3>
            <p><strong>{{ selectedContact.name }}</strong></p>
            <p>{{ selectedContact.email }}</p>
          </div>

          <div class="detail-section">
            <h3>موضوع:</h3>
            <p>{{ selectedContact.subject }}</p>
          </div>

          <div class="detail-section">
            <h3>پیام:</h3>
            <p class="message-text">{{ selectedContact.message }}</p>
          </div>

          <div class="detail-section">
            <h3>تاریخ ارسال:</h3>
            <p>{{ formatFullDate(selectedContact.created_at) }}</p>
          </div>

          <div class="modal-actions">
            <button 
              v-if="!selectedContact.read"
              @click="markAsRead(selectedContact.id)"
              class="btn-primary"
            >
              ✓ علامت‌گذاری به عنوان خوانده شده
            </button>
            <button @click="deleteContact(selectedContact.id)" class="btn-delete">
              🗑️ حذف پیام
            </button>
            <button @click="selectedContact = null" class="btn-secondary">
              بستن
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminService } from '../api/services'

const contacts = ref([])
const selectedContact = ref(null)
const loading = ref(false)

const unreadCount = computed(() => {
  return contacts.value.filter(c => !c.read).length
})

const loadContacts = async () => {
  loading.value = true
  try {
    contacts.value = await adminService.getContacts()
  } catch (error) {
    console.error('Failed to load contacts:', error)
    alert('خطا در بارگذاری پیام‌ها')
  } finally {
    loading.value = false
  }
}

const markAsRead = async (id) => {
  try {
    await adminService.markContactRead(id)
    selectedContact.value.read = true
    await loadContacts()
    alert('پیام به عنوان خوانده شده علامت‌گذاری شد')
  } catch (error) {
    alert('خطا: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  }
}

const deleteContact = async (id) => {
  if (!confirm('آیا از حذف این پیام مطمئن هستید؟')) return
  
  try {
    await adminService.deleteContact(id)
    selectedContact.value = null
    await loadContacts()
    alert('پیام با موفقیت حذف شد')
  } catch (error) {
    alert('خطا: ' + (error.response?.data?.detail || 'عملیات ناموفق'))
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('fa-IR')
}

const formatFullDate = (date) => {
  return new Date(date).toLocaleString('fa-IR')
}

onMounted(() => {
  loadContacts()
})
</script>

<style scoped>
.admin-contacts {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-card.alert {
  border: 2px solid #fbd38d;
  background: #fffaf0;
}

.info-card .label {
  color: #718096;
  font-size: 0.95rem;
}

.info-card .value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2d3748;
}

.info-card.alert .value {
  color: #c05621;
}

.contacts-list {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.loading,
.empty {
  text-align: center;
  color: #718096;
  padding: 3rem;
}

.contacts-container {
  max-height: 600px;
  overflow-y: auto;
}

.contact-card {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.contact-card:hover {
  background: #f7fafc;
}

.contact-card.unread {
  background: #fffaf0;
  border-left: 4px solid #f6ad55;
}

.contact-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.contact-name {
  font-weight: 600;
  color: #2d3748;
  font-size: 1rem;
}

.unread-badge {
  background: #fbd38d;
  color: #7c2d12;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.contact-email {
  color: #667eea;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.contact-subject {
  color: #4a5568;
  font-weight: 500;
  margin-bottom: 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.contact-date {
  color: #a0aec0;
  font-size: 0.85rem;
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
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #718096;
}

.contact-details {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-section h3 {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
  font-size: 0.95rem;
  text-transform: uppercase;
  font-weight: 600;
}

.detail-section p {
  margin: 0;
  color: #4a5568;
  line-height: 1.6;
}

.message-text {
  background: #f7fafc;
  padding: 1rem;
  border-radius: 8px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  flex-direction: column;
}

.btn-primary,
.btn-secondary,
.btn-delete {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: #e2e8f0;
  color: #2d3748;
}

.btn-secondary:hover {
  background: #cbd5e0;
}

.btn-delete {
  background: #fed7d7;
  color: #c53030;
}

.btn-delete:hover {
  background: #fc8181;
}

@media (max-width: 768px) {
  .header-info {
    grid-template-columns: 1fr;
  }

  .modal-card {
    width: 95%;
  }

  .contact-card {
    padding: 1rem;
  }

  .modal-actions {
    flex-direction: column;
  }
}
</style>
