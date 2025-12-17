<template>
  <div class="admin-comments">
    <div class="header">
      <h2>مدیریت نظرات</h2>
      <div class="stats-summary">
        <div class="stat-card">
          <span class="stat-label">کل نظرات</span>
          <span class="stat-value">{{ stats.total }}</span>
        </div>
        <div class="stat-card approved">
          <span class="stat-label">تایید شده</span>
          <span class="stat-value">{{ stats.approved }}</span>
        </div>
        <div class="stat-card pending">
          <span class="stat-label">در انتظار</span>
          <span class="stat-value">{{ stats.pending }}</span>
        </div>
        <div class="stat-card rating">
          <span class="stat-label">میانگین امتیاز</span>
          <span class="stat-value">{{ stats.average_rating }} ⭐</span>
        </div>
      </div>
    </div>

    <!-- فیلترها -->
    <div class="filters">
      <div class="filter-group">
        <label>وضعیت:</label>
        <select v-model="filter.status">
          <option value="all">همه</option>
          <option value="approved">تایید شده</option>
          <option value="pending">در انتظار تایید</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>نوع محتوا:</label>
        <select v-model="filter.contentType">
          <option value="">همه</option>
          <option value="article">مقالات</option>
          <option value="project">پروژه‌ها</option>
        </select>
      </div>
      
      <button @click="fetchComments" class="btn-refresh">
        🔄 بروزرسانی
      </button>
    </div>

    <!-- جدول نظرات -->
    <div class="table-container">
      <table v-if="!loading && filteredComments.length > 0">
        <thead>
          <tr>
            <th>شناسه</th>
            <th>نام</th>
            <th>ایمیل</th>
            <th>نظر</th>
            <th>امتیاز</th>
            <th>نوع</th>
            <th>وضعیت</th>
            <th>تاریخ</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="comment in filteredComments" :key="comment.id">
            <td>{{ comment.id }}</td>
            <td>{{ comment.name }}</td>
            <td>{{ comment.email }}</td>
            <td class="comment-content">
              {{ truncateText(comment.content, 50) }}
              <button 
                v-if="comment.content.length > 50" 
                @click="showFullComment(comment)"
                class="view-more"
              >
                بیشتر...
              </button>
            </td>
            <td>
              <div class="rating-display">
                <span class="stars">{{ '⭐'.repeat(comment.rating) }}</span>
                <span class="rating-number">({{ comment.rating }})</span>
              </div>
            </td>
            <td>
              <span class="badge" :class="comment.content_type">
                {{ comment.content_type === 'article' ? 'مقاله' : 'پروژه' }}
              </span>
            </td>
            <td>
              <span 
                class="status-badge" 
                :class="{ approved: comment.approved, pending: !comment.approved }"
              >
                {{ comment.approved ? 'تایید شده' : 'در انتظار' }}
              </span>
            </td>
            <td class="date-cell">{{ formatDate(comment.created_at) }}</td>
            <td class="actions">
              <button
                @click="toggleApprove(comment)"
                :class="['btn-action', comment.approved ? 'btn-warning' : 'btn-success']"
                :title="comment.approved ? 'لغو تایید' : 'تایید'"
              >
                {{ comment.approved ? '✗' : '✓' }}
              </button>
              <button
                @click="deleteCommentAction(comment.id)"
                class="btn-action btn-danger"
                title="حذف"
              >
                🗑
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>در حال بارگیری نظرات...</p>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && filteredComments.length === 0" class="empty-state">
        <p>
          {{ comments.length === 0 ? 'نظری یافت نشد' : 'هیچ نظری با فیلتر انتخاب شده وجود ندارد' }}
        </p>
      </div>
    </div>

    <!-- Modal نمایش/ویرایش نظر -->
    <div v-if="selectedComment" class="modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button @click="closeModal" class="modal-close">×</button>
        <h3>{{ isEditingComment ? 'ویرایش نظر' : 'جزئیات نظر' }}</h3>
        
        <!-- حالت نمایش -->
        <div v-if="!isEditingComment" class="comment-detail">
          <div class="detail-row">
            <strong>نام:</strong>
            <span>{{ selectedComment.name }}</span>
          </div>
          <div class="detail-row">
            <strong>ایمیل:</strong>
            <span>{{ selectedComment.email }}</span>
          </div>
          <div class="detail-row">
            <strong>امتیاز:</strong>
            <span class="stars">{{ '⭐'.repeat(selectedComment.rating) }} ({{ selectedComment.rating }}/5)</span>
          </div>
          <div class="detail-row">
            <strong>نوع:</strong>
            <span>{{ selectedComment.content_type === 'article' ? 'مقاله' : 'پروژه' }} #{{ selectedComment.content_id }}</span>
          </div>
          <div class="detail-row">
            <strong>تاریخ:</strong>
            <span>{{ new Date(selectedComment.created_at).toLocaleString('fa-IR') }}</span>
          </div>
          <div class="detail-row">
            <strong>وضعیت:</strong>
            <span 
              class="status-badge" 
              :class="{ approved: selectedComment.approved, pending: !selectedComment.approved }"
            >
              {{ selectedComment.approved ? 'تایید شده' : 'در انتظار تایید' }}
            </span>
          </div>
          <div class="detail-row full">
            <strong>متن نظر:</strong>
            <p class="comment-text">{{ selectedComment.content }}</p>
          </div>
        </div>

        <!-- حالت ویرایش -->
        <div v-else class="edit-form">
          <div class="form-group">
            <label>نام:</label>
            <input v-model="editFormData.name" type="text" placeholder="نام">
          </div>
          <div class="form-group">
            <label>ایمیل:</label>
            <input v-model="editFormData.email" type="email" placeholder="ایمیل">
          </div>
          <div class="form-group">
            <label>امتیاز:</label>
            <div class="rating-selector">
              <button
                v-for="n in 5"
                :key="n"
                @click="editFormData.rating = n"
                class="rating-btn"
                :class="{ active: editFormData.rating === n }"
              >
                ⭐ {{ n }}
              </button>
            </div>
          </div>
          <div class="form-group full">
            <label>متن نظر:</label>
            <textarea v-model="editFormData.content" placeholder="متن نظر" rows="6"></textarea>
          </div>
          <div class="form-group">
            <label>وضعیت تایید:</label>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input v-model="editFormData.approved" type="checkbox">
                <span>{{ editFormData.approved ? 'تایید شده' : 'در انتظار تایید' }}</span>
              </label>
            </div>
          </div>
        </div>
        
        <div class="modal-actions">
          <template v-if="!isEditingComment">
            <button
              @click="startEditComment()"
              class="btn btn-info"
            >
              ✎ ویرایش نظر
            </button>
            <button
              @click="toggleApprove(selectedComment); closeModal()"
              :class="['btn', selectedComment.approved ? 'btn-warning' : 'btn-success']"
            >
              {{ selectedComment.approved ? 'لغو تایید' : 'تایید نظر' }}
            </button>
            <button
              @click="deleteCommentAction(selectedComment.id); closeModal()"
              class="btn btn-danger"
            >
              حذف نظر
            </button>
          </template>
          <template v-else>
            <button
              @click="cancelEdit()"
              class="btn btn-secondary"
            >
              انصراف
            </button>
            <button
              @click="saveEditComment()"
              class="btn btn-success"
              :disabled="savingComment"
            >
              {{ savingComment ? 'در حال ذخیره...' : '✓ ذخیره تغییرات' }}
            </button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getComments, approveComment, deleteComment, getCommentStats, updateComment } from '../api/services'

const comments = ref([])
const stats = ref({
  total: 0,
  approved: 0,
  pending: 0,
  average_rating: 0
})
const loading = ref(false)
const selectedComment = ref(null)
const isEditingComment = ref(false)
const savingComment = ref(false)

const editFormData = ref({
  name: '',
  email: '',
  content: '',
  rating: 1,
  approved: false
})

const filter = ref({
  status: 'all',
  contentType: ''
})

const filteredComments = computed(() => {
  let result = comments.value

  // فیلتر وضعیت
  if (filter.value.status === 'approved') {
    result = result.filter(c => c.approved)
  } else if (filter.value.status === 'pending') {
    result = result.filter(c => !c.approved)
  }

  // فیلتر نوع محتوا
  if (filter.value.contentType) {
    result = result.filter(c => c.content_type === filter.value.contentType)
  }

  return result
})

const fetchComments = async () => {
  loading.value = true
  try {
    const allComments = await getComments({
      approved_only: false
    })
    comments.value = allComments || []
    
    // آمار
    const statsData = await getCommentStats()
    stats.value = statsData
  } catch (error) {
    console.error('Error fetching comments:', error)
  } finally {
    loading.value = false
  }
}

const toggleApprove = async (comment) => {
  try {
    const updated = await approveComment(comment.id)
    comment.approved = updated.approved
    
    // به‌روزرسانی آمار
    if (updated.approved) {
      stats.value.approved++
      stats.value.pending--
    } else {
      stats.value.approved--
      stats.value.pending++
    }
  } catch (error) {
    console.error('Error toggling approval:', error)
    alert('خطا در تغییر وضعیت نظر')
  }
}

const deleteCommentAction = async (commentId) => {
  if (!confirm('آیا از حذف این نظر اطمینان دارید؟')) {
    return
  }
  
  try {
    await deleteComment(commentId)
    comments.value = comments.value.filter(c => c.id !== commentId)
    stats.value.total--
    
    const deletedComment = comments.value.find(c => c.id === commentId)
    if (deletedComment && deletedComment.approved) {
      stats.value.approved--
    } else if (deletedComment) {
      stats.value.pending--
    }
  } catch (error) {
    console.error('Error deleting comment:', error)
    alert('خطا در حذف نظر')
  }
}

const showFullComment = (comment) => {
  selectedComment.value = comment
  isEditingComment.value = false
}

const startEditComment = () => {
  if (selectedComment.value) {
    editFormData.value = {
      name: selectedComment.value.name,
      email: selectedComment.value.email,
      content: selectedComment.value.content,
      rating: selectedComment.value.rating,
      approved: selectedComment.value.approved
    }
    isEditingComment.value = true
  }
}

const cancelEdit = () => {
  isEditingComment.value = false
  editFormData.value = {
    name: '',
    email: '',
    content: '',
    rating: 1,
    approved: false
  }
}

const saveEditComment = async () => {
  if (!selectedComment.value || !editFormData.value.name || !editFormData.value.email || !editFormData.value.content) {
    alert('لطفا تمام فیلدهای الزامی را پر کنید')
    return
  }

  savingComment.value = true
  try {
    console.log('Saving comment with data:', {
      id: selectedComment.value.id,
      data: {
        name: editFormData.value.name,
        email: editFormData.value.email,
        content: editFormData.value.content,
        rating: editFormData.value.rating,
        approved: editFormData.value.approved
      }
    })

    const updated = await updateComment(selectedComment.value.id, {
      name: editFormData.value.name,
      email: editFormData.value.email,
      content: editFormData.value.content,
      rating: editFormData.value.rating,
      approved: editFormData.value.approved
    })
    
    console.log('Updated comment response:', updated)
    
    // به‌روزرسانی کامنت در لیست
    const index = comments.value.findIndex(c => c.id === selectedComment.value.id)
    if (index !== -1) {
      const wasApproved = comments.value[index].approved
      comments.value[index] = updated
      
      // به‌روزرسانی آمار اگر وضعیت تایید تغییر کرد
      if (wasApproved && !updated.approved) {
        stats.value.approved--
        stats.value.pending++
      } else if (!wasApproved && updated.approved) {
        stats.value.approved++
        stats.value.pending--
      }
    }
    
    selectedComment.value = updated
    isEditingComment.value = false
    alert('نظر با موفقیت به‌روزرسانی شد')
  } catch (error) {
    console.error('Error updating comment:', error)
    console.error('Error response:', error.response?.data)
    alert(`خطا در ویرایش نظر: ${error.response?.data?.detail || error.message}`)
  } finally {
    savingComment.value = false
  }
}

const closeModal = () => {
  selectedComment.value = null
  isEditingComment.value = false
}

const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchComments()
})
</script>

<style scoped>
.admin-comments {
  padding: 2rem;
  direction: rtl;
}

.header {
  margin-bottom: 2rem;
}

.header h2 {
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-card.approved {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-card.pending {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-card.rating {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
}

/* فیلترها */
.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #374151;
}

.filter-group select {
  padding: 0.5rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-family: inherit;
}

.btn-refresh {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

/* جدول */
.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f9fafb;
}

th {
  padding: 1rem;
  text-align: right;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
}

tr:hover {
  background: #f9fafb;
}

.comment-content {
  max-width: 300px;
}

.view-more {
  color: #3b82f6;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 600;
  padding: 0;
  margin-right: 0.25rem;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stars {
  font-size: 1rem;
}

.rating-number {
  font-size: 0.875rem;
  color: #6b7280;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.badge.article {
  background: #dbeafe;
  color: #1e40af;
}

.badge.project {
  background: #dcfce7;
  color: #166534;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-badge.approved {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.pending {
  background: #fed7aa;
  color: #92400e;
}

.date-cell {
  font-size: 0.875rem;
  color: #6b7280;
  white-space: nowrap;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-action {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.btn-action:hover {
  transform: scale(1.1);
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-warning {
  background: #f59e0b;
  color: white;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

/* Loading & Empty States */
.loading-state,
.empty-state {
  padding: 4rem 2rem;
  text-align: center;
  color: #6b7280;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Modal */
.modal {
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
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 1rem;
  left: 1rem;
  width: 32px;
  height: 32px;
  border: none;
  background: #f3f4f6;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
}

.modal-close:hover {
  background: #e5e7eb;
}

.modal-content h3 {
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.comment-detail {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-row {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 1rem;
}

.detail-row.full {
  grid-template-columns: 1fr;
}

.detail-row strong {
  color: #374151;
}

.comment-text {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 8px;
  line-height: 1.7;
  white-space: pre-wrap;
  margin-top: 0.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: flex-end;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-info {
  background: #06b6d4;
}

.btn-info:hover {
  background: #0891b2;
}

.btn-secondary {
  background: #6b7280;
}

.btn-secondary:hover {
  background: #4b5563;
}

/* Edit Form */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group textarea {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-family: inherit;
  font-size: 1rem;
  transition: border-color 0.2s;
  direction: rtl;
  text-align: right;
}

.form-group input[type="text"]:focus,
.form-group input[type="email"]:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group.full {
  grid-column: 1 / -1;
}

.rating-selector {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.rating-btn {
  padding: 0.5rem 1rem;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  color: #6b7280;
  transition: all 0.2s;
}

.rating-btn:hover {
  border-color: #f59e0b;
  color: #f59e0b;
}

.rating-btn.active {
  background: #fef3c7;
  border-color: #f59e0b;
  color: #d97706;
}

.checkbox-group {
  display: flex;
  gap: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  color: #374151;
}

.checkbox-label input[type="checkbox"] {
  cursor: pointer;
  width: 18px;
  height: 18px;
}

/* Responsive */
@media (max-width: 1024px) {
  .comment-content {
    max-width: 150px;
  }

  th, td {
    padding: 0.75rem 0.5rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 768px) {
  .admin-comments {
    padding: 1rem;
  }

  .header h2 {
    font-size: 1.5rem;
  }

  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .filters {
    flex-direction: column;
  }

  .filter-group {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-group select {
    width: 100%;
  }

  .btn-refresh {
    width: 100%;
  }

  .table-container {
    overflow-x: auto;
    border-radius: 8px;
  }

  table {
    min-width: 100%;
    font-size: 0.75rem;
  }

  th, td {
    padding: 0.5rem;
  }

  .comment-content {
    max-width: 80px;
    word-break: break-word;
  }

  .view-more {
    display: block;
    margin-top: 0.25rem;
  }

  .actions {
    flex-direction: column;
    gap: 0.25rem;
  }

  .btn-action {
    width: 30px;
    height: 30px;
    padding: 0;
    font-size: 0.875rem;
  }

  .detail-row {
    grid-template-columns: 1fr;
  }

  .modal-content {
    padding: 1.5rem;
    max-width: 90%;
  }

  .modal-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .admin-comments {
    padding: 0.5rem;
  }

  .header h2 {
    font-size: 1.25rem;
  }

  .stats-summary {
    grid-template-columns: 1fr;
  }

  .stat-label {
    font-size: 0.75rem;
  }

  .stat-value {
    font-size: 1.25rem;
  }

  .filters {
    gap: 0.5rem;
  }

  .filter-group {
    gap: 0.25rem;
  }

  .filter-group select {
    padding: 0.375rem 0.5rem;
    font-size: 0.875rem;
  }

  .btn-refresh {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
  }

  .table-container {
    border-radius: 8px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  }

  table {
    font-size: 0.65rem;
  }

  th {
    padding: 0.4rem 0.3rem;
    border-bottom: 1px solid #e5e7eb;
  }

  td {
    padding: 0.3rem;
    border-bottom: 1px solid #f3f4f6;
  }

  .comment-content {
    max-width: 50px;
  }

  .rating-number {
    display: none;
  }

  .stars {
    font-size: 0.75rem;
  }

  .badge {
    padding: 0.1rem 0.5rem;
    font-size: 0.65rem;
  }

  .status-badge {
    padding: 0.1rem 0.5rem;
    font-size: 0.65rem;
  }

  .date-cell {
    font-size: 0.65rem;
  }

  .btn-action {
    width: 24px;
    height: 24px;
    font-size: 0.75rem;
  }

  .modal-content {
    padding: 1rem;
    border-radius: 12px;
  }

  .modal-close {
    width: 28px;
    height: 28px;
    font-size: 1.25rem;
  }

  .detail-row {
    gap: 0.5rem;
  }

  .detail-row strong {
    min-width: 60px;
  }

  .form-group input,
  .form-group select,
  .form-group textarea {
    font-size: 16px;
  }
}
</style>
