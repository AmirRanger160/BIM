<template>
  <div class="admin-contacts" :class="sidebarClasses">
    <ToastContainer />
    <AdminSidebar @navigate="handleNavigation" @sidebar-state-change="handleSidebarStateChange" />
    <div class="main-content">
      <div class="admin-header">
        <div class="header-title">
          <h1>مدیریت تماس‌ها</h1>
          <span class="badge">{{ submissions.length }}</span>
        </div>
        <button @click="logout" class="btn-logout">خروج</button>
      </div>

      <div class="admin-body">
        <!-- Filters -->
        <div class="filters">
          <div class="filter-group">
            <label>فیلتر بر اساس وضعیت:</label>
            <select v-model="statusFilter" @change="loadSubmissions">
              <option value="">همه</option>
              <option value="new">جدید</option>
              <option value="read">خوانده شده</option>
              <option value="replied">پاسخ داده شده</option>
              <option value="archived">آرشیو شده</option>
            </select>
          </div>
          <button @click="loadSubmissions" class="btn-refresh">
            🔄 بارگذاری مجدد
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="loading">
          <Loader />
          <p>در حال بارگذاری تماس‌ها...</p>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <!-- Submissions Table -->
        <div v-if="!isLoading && submissions.length > 0" class="submissions-table">
          <div class="table-header">
            <div class="col-checkbox">
              <input 
                type="checkbox" 
                :checked="allSelected"
                @change="toggleSelectAll"
              >
            </div>
            <div class="col-name">نام</div>
            <div class="col-email">ایمیل</div>
            <div class="col-phone">تلفن</div>
            <div class="col-date">تاریخ</div>
            <div class="col-status">وضعیت</div>
            <div class="col-actions">عملیات</div>
          </div>
          
          <div 
            v-for="submission in submissions" 
            :key="submission.id"
            class="table-row"
            :class="{ selected: selectedSubmissions.includes(submission.id) }"
          >
            <div class="col-checkbox">
              <input 
                type="checkbox" 
                :checked="selectedSubmissions.includes(submission.id)"
                @change="toggleSelection(submission.id)"
              >
            </div>
            <div class="col-name">{{ submission.name }}</div>
            <div class="col-email">{{ submission.email }}</div>
            <div class="col-phone">{{ submission.phone }}</div>
            <div class="col-date">{{ formatDate(submission.submitted_at) }}</div>
            <div class="col-status">
              <select 
                :value="submission.status"
                @change="(e) => updateStatus(submission.id, e.target.value)"
                class="status-select"
                :class="`status-${submission.status}`"
              >
                <option value="new">جدید</option>
                <option value="read">خوانده شده</option>
                <option value="replied">پاسخ داده شده</option>
                <option value="archived">آرشیو شده</option>
              </select>
            </div>
            <div class="col-actions">
              <button 
                @click="viewSubmission(submission)"
                class="btn-action btn-view"
                title="مشاهده"
              >
                👁️
              </button>
              <button 
                @click="deleteSubmission(submission.id)"
                class="btn-action btn-delete"
                title="حذف"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!isLoading && submissions.length === 0" class="empty-state">
          <div class="empty-icon">📭</div>
          <p>هیچ تماسی یافت نشد</p>
        </div>
      </div>

      <!-- Detail Modal -->
      <div v-if="selectedSubmission" class="modal-overlay" @click="closeModal">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h2>جزئیات تماس</h2>
            <button @click="closeModal" class="btn-close">✕</button>
          </div>
          <div class="modal-body">
            <div class="detail-item">
              <span class="label">نام:</span>
              <span class="value">{{ selectedSubmission.name }}</span>
            </div>
            <div class="detail-item">
              <span class="label">ایمیل:</span>
              <span class="value">
                <a :href="`mailto:${selectedSubmission.email}`">{{ selectedSubmission.email }}</a>
              </span>
            </div>
            <div class="detail-item">
              <span class="label">تلفن:</span>
              <span class="value">
                <a :href="`tel:${selectedSubmission.phone}`">{{ selectedSubmission.phone }}</a>
              </span>
            </div>
            <div class="detail-item">
              <span class="label">تاریخ ارسال:</span>
              <span class="value">{{ formatDateTime(selectedSubmission.submitted_at) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">آدرس IP:</span>
              <span class="value">{{ selectedSubmission.ip_address || 'نامشخص' }}</span>
            </div>
            <div class="detail-item">
              <span class="label">وضعیت:</span>
              <span class="value badge" :class="`badge-${selectedSubmission.status}`">
                {{ getStatusText(selectedSubmission.status) }}
              </span>
            </div>
            <div class="detail-item full-width">
              <span class="label">پیام:</span>
              <div class="message-box">
                {{ selectedSubmission.message }}
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="deleteSubmission(selectedSubmission.id)" class="btn btn-danger">
              حذف
            </button>
            <button @click="closeModal" class="btn btn-primary">
              بستن
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminSidebar from './AdminSidebar.vue'
import ToastContainer from './ToastContainer.vue'
import Loader from './Loader.vue'
import { adminContactService } from '../services/api'

export default {
  name: 'AdminContacts',
  components: {
    AdminSidebar,
    ToastContainer,
    Loader
  },
  data() {
    return {
      submissions: [],
      isLoading: false,
      errorMessage: '',
      statusFilter: '',
      selectedSubmissions: [],
      selectedSubmission: null,
      sidebarState: {
        isOpen: true,
        isMobile: false
      }
    }
  },
  computed: {
    sidebarClasses() {
      const classes = [];
      if (!this.sidebarState.isOpen && !this.sidebarState.isMobile) {
        classes.push('sidebar-collapsed');
      }
      if (this.sidebarState.isMobile && !this.sidebarState.isOpen) {
        classes.push('sidebar-closed');
      }
      return classes;
    },
    allSelected() {
      return this.selectedSubmissions.length === this.submissions.length && this.submissions.length > 0;
    }
  },
  inject: ['navigateTo'],
  mounted() {
    this.checkAuth();
    this.loadSubmissions();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('admin_token');
      if (!token) {
        this.navigateTo('/admin/login');
      }
    },
    async loadSubmissions() {
      this.isLoading = true;
      this.errorMessage = '';
      try {
        const response = await adminContactService.getAll({
          status_filter: this.statusFilter || undefined
        });
        this.submissions = response.data || [];
        this.selectedSubmissions = [];
      } catch (error) {
        console.error('Error loading submissions:', error);
        this.errorMessage = 'خطا در بارگذاری تماس‌ها. لطفا دوباره تلاش کنید.';
      } finally {
        this.isLoading = false;
      }
    },
    async updateStatus(id, status) {
      try {
        await adminContactService.updateStatus(id, { status });
        const submission = this.submissions.find(s => s.id === id);
        if (submission) {
          submission.status = status;
        }
      } catch (error) {
        console.error('Error updating status:', error);
        this.errorMessage = 'خطا در به‌روزرسانی وضعیت';
      }
    },
    async deleteSubmission(id) {
      if (!confirm('آیا مطمئن هستید که می‌خواهید این تماس را حذف کنید؟')) {
        return;
      }
      try {
        await adminContactService.delete(id);
        this.submissions = this.submissions.filter(s => s.id !== id);
        this.selectedSubmissions = this.selectedSubmissions.filter(sId => sId !== id);
        if (this.selectedSubmission?.id === id) {
          this.closeModal();
        }
      } catch (error) {
        console.error('Error deleting submission:', error);
        this.errorMessage = 'خطا در حذف تماس';
      }
    },
    viewSubmission(submission) {
      this.selectedSubmission = submission;
    },
    closeModal() {
      this.selectedSubmission = null;
    },
    toggleSelection(id) {
      const index = this.selectedSubmissions.indexOf(id);
      if (index > -1) {
        this.selectedSubmissions.splice(index, 1);
      } else {
        this.selectedSubmissions.push(id);
      }
    },
    toggleSelectAll() {
      if (this.allSelected) {
        this.selectedSubmissions = [];
      } else {
        this.selectedSubmissions = this.submissions.map(s => s.id);
      }
    },
    formatDate(date) {
      if (!date) return '-';
      return new Date(date).toLocaleDateString('fa-IR');
    },
    formatDateTime(date) {
      if (!date) return '-';
      const d = new Date(date);
      return d.toLocaleString('fa-IR');
    },
    getStatusText(status) {
      const statusMap = {
        'new': 'جدید',
        'read': 'خوانده شده',
        'replied': 'پاسخ داده شده',
        'archived': 'آرشیو شده'
      };
      return statusMap[status] || status;
    },
    handleNavigation(route) {
      this.navigateTo(route);
    },
    handleSidebarStateChange(state) {
      this.sidebarState = { ...state };
    },
    logout() {
      localStorage.removeItem('admin_token');
      this.navigateTo('/admin/login');
    }
  }
}
</script>

<style scoped>
.admin-contacts {
  display: flex;
  min-height: 100vh;
  background: #f5f5f5;
  direction: rtl;
  --sidebar-width: 280px;
  --sidebar-collapsed-width: 70px;
  --sidebar-margin: var(--sidebar-width);
}

.admin-contacts.sidebar-collapsed {
  --sidebar-margin: var(--sidebar-collapsed-width);
}

.admin-contacts.sidebar-closed {
  --sidebar-margin: 0px;
}

.main-content {
  flex: 1;
  padding: 20px;
  margin-right: var(--sidebar-margin);
  transition: margin-right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-title h1 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

.badge {
  display: inline-block;
  background: #3498db;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.btn-logout {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s ease;
}

.btn-logout:hover {
  background: #c0392b;
}

.admin-body {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-group label {
  font-weight: 600;
  color: #333;
}

.filter-group select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 14px;
}

.btn-refresh {
  padding: 8px 16px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s ease;
}

.btn-refresh:hover {
  background: #229954;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  gap: 20px;
}

.error-message {
  padding: 15px;
  background: #fee;
  color: #c33;
  border-left: 4px solid #c33;
  border-radius: 4px;
  margin-bottom: 20px;
}

.submissions-table {
  overflow-x: auto;
}

.table-header {
  display: grid;
  grid-template-columns: 40px 150px 180px 130px 130px 120px 100px;
  gap: 10px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #dee2e6;
  position: sticky;
  top: 0;
  z-index: 10;
}

.table-row {
  display: grid;
  grid-template-columns: 40px 150px 180px 130px 130px 120px 100px;
  gap: 10px;
  padding: 15px;
  border-bottom: 1px solid #eee;
  align-items: center;
  transition: background 0.2s ease;
}

.table-row:hover {
  background: #f9f9f9;
}

.table-row.selected {
  background: #e3f2fd;
}

.col-checkbox {
  text-align: center;
}

.col-checkbox input {
  cursor: pointer;
  width: 18px;
  height: 18px;
}

.col-name,
.col-email,
.col-phone,
.col-date,
.col-status,
.col-actions {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
}

.col-email {
  color: #0066cc;
}

.status-select {
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 12px;
  width: 100%;
}

.status-select.status-new {
  color: #d97706;
}

.status-select.status-read {
  color: #3b82f6;
}

.status-select.status-replied {
  color: #10b981;
}

.status-select.status-archived {
  color: #6b7280;
}

.btn-action {
  padding: 6px 10px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  transition: transform 0.2s ease;
  margin: 0 4px;
}

.btn-action:hover {
  transform: scale(1.2);
}

.btn-view {
  color: #3498db;
}

.btn-delete {
  color: #e74c3c;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.empty-state p {
  color: #999;
  font-size: 16px;
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
  z-index: 100;
  direction: rtl;
}

.modal {
  background: white;
  border-radius: 8px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 20px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  transition: color 0.2s ease;
}

.btn-close:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.detail-item {
  display: flex;
  margin-bottom: 20px;
  gap: 15px;
}

.detail-item.full-width {
  flex-direction: column;
}

.detail-item .label {
  font-weight: 600;
  color: #333;
  min-width: 120px;
  flex-shrink: 0;
}

.detail-item .value {
  color: #666;
  word-break: break-word;
}

.detail-item a {
  color: #0066cc;
  text-decoration: none;
}

.detail-item a:hover {
  text-decoration: underline;
}

.message-box {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  border-left: 4px solid #3498db;
  white-space: pre-wrap;
  word-wrap: break-word;
  line-height: 1.6;
  color: #555;
}

.badge-new {
  background: #d97706;
}

.badge-read {
  background: #3b82f6;
}

.badge-replied {
  background: #10b981;
}

.badge-archived {
  background: #6b7280;
}

.modal-footer {
  display: flex;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #eee;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s ease;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background: #c0392b;
}

@media (max-width: 1024px) {
  .table-header,
  .table-row {
    grid-template-columns: 40px 120px 140px 100px 100px 100px 80px;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 10px;
  }

  .admin-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .filters {
    flex-direction: column;
  }

  .table-header,
  .table-row {
    grid-template-columns: 40px 100px 120px 90px 90px 90px 60px;
    font-size: 12px;
    gap: 5px;
    padding: 10px;
  }

  .col-name,
  .col-email,
  .col-phone,
  .col-date,
  .col-status,
  .col-actions {
    font-size: 12px;
  }

  .btn-action {
    padding: 4px 6px;
    margin: 0 2px;
    font-size: 14px;
  }
}
</style>
