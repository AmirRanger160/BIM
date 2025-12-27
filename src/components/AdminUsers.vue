<template>
  <div class="admin-users" :class="sidebarClasses">
    <AdminSidebar @navigate="handleNavigation" @sidebar-state-change="handleSidebarStateChange" />
    <div class="main-content">
      <div class="content-header">
        <h1>مدیریت کاربران</h1>
        <button @click="showAddForm" class="btn-primary">افزودن کاربر</button>
      </div>

      <div class="content-body">
        <!-- List View -->
        <div v-if="!showForm" class="list-view">
          <AdminTable
            :data="users"
            :columns="columns"
            :loading="loading"
            @edit="editUser"
            @delete="deleteUser"
            @change-password="openChangePasswordDialog"
          />
        </div>

        <!-- Form View -->
        <div v-else class="form-view">
          <form @submit.prevent="saveUser" class="user-form">
            <div class="form-grid">
              <div class="form-group">
                <label for="username">نام کاربری</label>
                <input
                  id="username"
                  v-model="formData.username"
                  type="text"
                  placeholder="نام کاربری"
                  required
                >
              </div>

              <div class="form-group">
                <label for="email">ایمیل</label>
                <input
                  id="email"
                  v-model="formData.email"
                  type="email"
                  placeholder="email@example.com"
                  required
                >
              </div>

              <div v-if="!editingUser" class="form-group">
                <label for="password">رمز عبور</label>
                <input
                  id="password"
                  v-model="formData.password"
                  type="password"
                  placeholder="رمز عبور"
                  required
                >
              </div>

              <div class="form-group">
                <label for="is_admin" class="checkbox-label">
                  <input
                    id="is_admin"
                    v-model="formData.is_admin"
                    type="checkbox"
                  >
                  دسترسی ادمین
                </label>
              </div>

              <div class="form-group">
                <label for="is_active" class="checkbox-label">
                  <input
                    id="is_active"
                    v-model="formData.is_active"
                    type="checkbox"
                  >
                  حساب فعال
                </label>
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn-save" :disabled="saving">
                {{ saving ? 'در حال ذخیره...' : 'ذخیره' }}
              </button>
              <button type="button" @click="cancelForm" class="btn-cancel">
                لغو
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Change Password Dialog -->
    <ChangePasswordDialog
      :is-open="showChangePasswordDialog"
      :user-id="selectedUserId"
      @close="showChangePasswordDialog = false"
      @success="handlePasswordChangeSuccess"
    />
  </div>
</template>

<script>
import AdminSidebar from './AdminSidebar.vue'
import AdminTable from './AdminTable.vue'
import ChangePasswordDialog from './ChangePasswordDialog.vue'
import { adminUserService } from '../services/api'

export default {
  name: 'AdminUsers',
  components: {
    AdminSidebar,
    AdminTable,
    ChangePasswordDialog
  },
  data() {
    return {
      users: [],
      loading: false,
      showForm: false,
      editingUser: null,
      saving: false,
      showChangePasswordDialog: false,
      selectedUserId: null,
      formData: {
        username: '',
        email: '',
        password: '',
        is_admin: false,
        is_active: true
      },
      columns: [
        { key: 'username', label: 'نام کاربری' },
        { key: 'email', label: 'ایمیل' },
        { key: 'is_admin', label: 'ادمین', type: 'boolean' },
        { key: 'is_active', label: 'فعال', type: 'boolean' },
        { key: 'created_at', label: 'تاریخ ایجاد', type: 'date' }
      ],
      sidebarState: {
        isOpen: true,
        isMobile: false
      }
    }
  },
  provide() {
    return {
      navigateTo: this.navigateTo
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
    }
  },
  inject: ['navigateTo'],
  mounted() {
    this.checkAuth();
    this.loadUsers();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('admin_token');
      if (!token) {
        this.navigateTo('/admin/login');
      }
    },
    async loadUsers() {
      this.loading = true;
      try {
        const response = await adminUserService.getAll();
        this.users = response.data;
      } catch (error) {
        console.error('Error loading users:', error);
      } finally {
        this.loading = false;
      }
    },
    showAddForm() {
      this.editingUser = null;
      this.formData = {
        username: '',
        email: '',
        password: '',
        is_admin: false,
        is_active: true
      };
      this.showForm = true;
    },
    editUser(user) {
      this.editingUser = user;
      this.formData = {
        username: user.username,
        email: user.email,
        password: '', // Don't populate password for security
        is_admin: user.is_admin,
        is_active: user.is_active
      };
      this.showForm = true;
    },
    cancelForm() {
      this.showForm = false;
      this.editingUser = null;
    },
    async saveUser() {
      this.saving = true;
      try {
        if (this.editingUser) {
          await adminUserService.update(this.editingUser.id, this.formData);
        } else {
          await adminUserService.create(this.formData);
        }
        this.cancelForm();
        this.loadUsers();
      } catch (error) {
        console.error('Error saving user:', error);
        alert('خطا در ذخیره کاربر. لطفا دوباره تلاش کنید.');
      } finally {
        this.saving = false;
      }
    },
    async deleteUser(user) {
      if (confirm(`آیا مطمئن هستید که می‌خواهید کاربر "${user.username}" را حذف کنید؟`)) {
        try {
          await adminUserService.delete(user.id);
          this.loadUsers();
        } catch (error) {
          console.error('Error deleting user:', error);
          alert('خطا در حذف کاربر. لطفا دوباره تلاش کنید.');
        }
      }
    },
    openChangePasswordDialog(user) {
      this.selectedUserId = user.id;
      this.showChangePasswordDialog = true;
    },
    handlePasswordChangeSuccess() {
      this.loadUsers();
      alert('رمز عبور با موفقیت تغییر یافت.');
    },
    handleNavigation(route) {
      this.navigateTo(route);
    },
    handleSidebarStateChange(state) {
      this.sidebarState = { ...state };
    }
  }
}
</script>

<style scoped>
.admin-users {
  display: flex;
  min-height: 100vh;
  background: #f5f5f5;
  direction: rtl;
  --sidebar-width: 280px;
  --sidebar-collapsed-width: 70px;
  --sidebar-margin: var(--sidebar-width);
}

.admin-users.sidebar-collapsed {
  --sidebar-margin: var(--sidebar-collapsed-width);
}

.admin-users.sidebar-closed {
  --sidebar-margin: 0px;
}

.main-content {
  flex: 1;
  padding: 20px;
  margin-right: var(--sidebar-margin);
  transition: margin-right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.content-header h1 {
  margin: 0;
  color: #333;
}

.btn-primary {
  background: #0099FF;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s ease;
}

.btn-primary:hover {
  background: #0077cc;
}

.content-body {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.list-view,
.form-view {
  padding: 20px;
}

.user-form {
  max-width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
  font-size: 14px;
}

.form-group input {
  padding: 10px 12px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #0099FF;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: normal !important;
  margin-bottom: 0 !important;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn-save,
.btn-cancel {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-save {
  background: #1abc9c;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #16a085;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #95a5a6;
  color: white;
}

.btn-cancel:hover {
  background: #7f8c8d;
}

@media (max-width: 768px) {
  .main-content {
    margin-right: 0;
    padding: 15px;
  }

  .content-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .content-header h1 {
    font-size: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-save,
  .btn-cancel {
    width: 100%;
  }
}
</style>