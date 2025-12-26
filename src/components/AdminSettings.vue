<template>
  <div class="admin-settings" :class="sidebarClasses">
    <AdminSidebar @navigate="handleNavigation" @sidebar-state-change="handleSidebarStateChange" />
    <div class="main-content">
      <div class="settings-header">
        <h1>تنظیمات</h1>
      </div>

      <div class="settings-content">
        <!-- Company Info Section -->
        <div class="settings-section">
          <h2>اطلاعات شرکت</h2>
          <form @submit.prevent="saveCompanyInfo" class="settings-form">
            <div class="form-grid">
              <div class="form-group">
                <label for="company-name">نام شرکت</label>
                <input
                  id="company-name"
                  v-model="companyInfo.name"
                  type="text"
                  placeholder="نام شرکت"
                >
              </div>
              <div class="form-group">
                <label for="company-location">آدرس</label>
                <input
                  id="company-location"
                  v-model="companyInfo.location"
                  type="text"
                  placeholder="آدرس شرکت"
                >
              </div>
              <div class="form-group">
                <label for="company-phone">تلفن</label>
                <input
                  id="company-phone"
                  v-model="companyInfo.phone"
                  type="tel"
                  placeholder="شماره تلفن"
                >
              </div>
              <div class="form-group">
                <label for="company-email">ایمیل</label>
                <input
                  id="company-email"
                  v-model="companyInfo.email"
                  type="email"
                  placeholder="ایمیل شرکت"
                >
              </div>
              <div class="form-group">
                <label for="company-founded">سال تاسیس</label>
                <input
                  id="company-founded"
                  v-model="companyInfo.founded_year"
                  type="number"
                  placeholder="سال تاسیس"
                >
              </div>
            </div>
            <button type="submit" class="btn-save" :disabled="savingCompany">
              {{ savingCompany ? 'در حال ذخیره...' : 'ذخیره اطلاعات شرکت' }}
            </button>
          </form>
        </div>

        <!-- Statistics Section -->
        <div class="settings-section">
          <h2>آمار</h2>
          <form @submit.prevent="saveStatistics" class="settings-form">
            <div class="form-grid">
              <div class="form-group">
                <label for="projects-count">تعداد پروژه‌ها</label>
                <input
                  id="projects-count"
                  v-model.number="statistics.annual_projects"
                  type="number"
                  placeholder="تعداد پروژه‌های سالانه"
                >
              </div>
              <div class="form-group">
                <label for="services-count">تعداد خدمات</label>
                <input
                  id="services-count"
                  v-model.number="statistics.service_types"
                  type="number"
                  placeholder="تعداد انواع خدمات"
                >
              </div>
              <div class="form-group">
                <label for="employees-count">تعداد کارکنان</label>
                <input
                  id="employees-count"
                  v-model.number="statistics.employees"
                  type="number"
                  placeholder="تعداد کارکنان"
                >
              </div>
              <div class="form-group">
                <label for="clients-count">مشتریان راضی</label>
                <input
                  id="clients-count"
                  v-model.number="statistics.satisfied_clients"
                  type="number"
                  placeholder="تعداد مشتریان راضی"
                >
              </div>
            </div>
            <button type="submit" class="btn-save" :disabled="savingStats">
              {{ savingStats ? 'در حال ذخیره...' : 'ذخیره آمار' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminSidebar from './AdminSidebar.vue'
import { adminSettingsService } from '../services/api'

export default {
  name: 'AdminSettings',
  components: {
    AdminSidebar
  },
  data() {
    return {
      companyInfo: {
        name: '',
        location: '',
        phone: '',
        email: '',
        founded_year: ''
      },
      statistics: {
        annual_projects: 0,
        service_types: 0,
        employees: 0,
        satisfied_clients: 0
      },
      savingCompany: false,
      savingStats: false,
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
    this.loadSettings();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('admin_token');
      if (!token) {
        this.navigateTo('/admin/login');
      }
    },
    async loadSettings() {
      try {
        const [companyResponse, statsResponse] = await Promise.all([
          adminSettingsService.getCompanyInfo(),
          adminSettingsService.getStatistics()
        ]);

        this.companyInfo = companyResponse.data;
        this.statistics = statsResponse.data;
      } catch (error) {
        console.error('Error loading settings:', error);
      }
    },
    async saveCompanyInfo() {
      this.savingCompany = true;
      try {
        await adminSettingsService.updateCompanyInfo(this.companyInfo);
        alert('اطلاعات شرکت با موفقیت ذخیره شد');
      } catch (error) {
        console.error('Error saving company info:', error);
        alert('خطا در ذخیره اطلاعات شرکت');
      } finally {
        this.savingCompany = false;
      }
    },
    async saveStatistics() {
      this.savingStats = true;
      try {
        await adminSettingsService.updateStatistics(this.statistics);
        alert('آمار با موفقیت ذخیره شد');
      } catch (error) {
        console.error('Error saving statistics:', error);
        alert('خطا در ذخیره آمار');
      } finally {
        this.savingStats = false;
      }
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
.admin-settings {
  display: flex;
  min-height: 100vh;
  background: #f5f5f5;
  direction: rtl;
  --sidebar-width: 280px;
  --sidebar-collapsed-width: 70px;
  --sidebar-margin: var(--sidebar-width);
}

.admin-settings.sidebar-collapsed {
  --sidebar-margin: var(--sidebar-collapsed-width);
}

.admin-settings.sidebar-closed {
  --sidebar-margin: 0px;
}

.main-content {
  flex: 1;
  padding: 20px;
  margin-right: var(--sidebar-margin);
  transition: margin-right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.settings-header {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.settings-header h1 {
  margin: 0;
  color: #333;
}

.settings-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.settings-section {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.settings-section h2 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
  border-bottom: 2px solid #1abc9c;
  padding-bottom: 10px;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
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
  border-color: #1abc9c;
}

.btn-save {
  background: #1abc9c;
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  align-self: flex-start;
  transition: all 0.3s ease;
}

.btn-save:hover:not(:disabled) {
  background: #16a085;
  transform: translateY(-1px);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .main-content {
    margin-right: 0;
    padding: 15px;
  }

  .settings-section {
    padding: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .btn-save {
    align-self: stretch;
  }
}
</style>