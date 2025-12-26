<template>
  <div class="admin-dashboard" :class="sidebarClasses">
    <AdminSidebar @navigate="handleNavigation" @sidebar-state-change="handleSidebarStateChange" />
    <div class="main-content">
      <div class="dashboard-header">
        <h1>داشبورد مدیریت</h1>
        <button @click="logout" class="btn-logout">خروج</button>
      </div>
      <div class="dashboard-content">
        <DashboardStats :stats="stats" />
        <div class="recent-activity">
          <h2>فعالیت‌های اخیر</h2>
          <div class="activity-list">
            <div class="activity-item">
              <span class="activity-time">۱۴:۳۰</span>
              <span class="activity-text">مقاله جدید اضافه شد: "نقش BIM در مهندسی"</span>
            </div>
            <div class="activity-item">
              <span class="activity-time">۱۴:۰۰</span>
              <span class="activity-text">پاسخ به تماس مشتری با شماره ۰۹۱۲...</span>
            </div>
            <div class="activity-item">
              <span class="activity-time">۱۳:۴۵</span>
              <span class="activity-text">پروژه جدید ثبت شد</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminSidebar from './AdminSidebar.vue'
import DashboardStats from './DashboardStats.vue'
import { adminSettingsService } from '../services/api'

export default {
  name: 'AdminDashboard',
  components: {
    AdminSidebar,
    DashboardStats
  },
  data() {
    return {
      stats: {
        articles: { total: 0, published: 0 },
        projects: 0,
        contacts: { total: 0, new: 0 },
        team: 0
      },
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
    }
  },
  provide() {
    return {
      navigateTo: this.navigateTo
    }
  },
  inject: ['navigateTo'],
  mounted() {
    this.checkAuth();
    this.loadStats();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('admin_token');
      if (!token) {
        this.navigateTo('/admin/login');
      }
    },
    async loadStats() {
      try {
        // Load statistics from API
        const statsResponse = await adminSettingsService.getStatistics();
        const statsData = statsResponse.data;

        // This would need actual API calls to get counts
        // For now, using placeholder data
        this.stats = {
          articles: { total: 25, published: 22 },
          projects: statsData.annual_projects || 1000,
          contacts: { total: 45, new: 12 },
          team: statsData.employees || 90
        };
      } catch (error) {
        console.error('Error loading stats:', error);
      }
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
.admin-dashboard {
  display: flex;
  min-height: 100vh;
  background: #f5f5f5;
  direction: rtl;
  --sidebar-width: 280px;
  --sidebar-collapsed-width: 70px;
  --sidebar-margin: var(--sidebar-width);
}

.admin-dashboard.sidebar-collapsed {
  --sidebar-margin: var(--sidebar-collapsed-width);
}

.admin-dashboard.sidebar-closed {
  --sidebar-margin: 0px;
}

.main-content {
  flex: 1;
  padding: 20px;
  margin-right: var(--sidebar-margin);
  transition: margin-right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.dashboard-header h1 {
  margin: 0;
  color: #333;
  font-size: 24px;
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

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.recent-activity {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.recent-activity h2 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  font-size: 12px;
  color: #666;
  font-weight: bold;
  min-width: 50px;
}

.activity-text {
  color: #333;
  font-size: 14px;
}

@media (max-width: 768px) {
  .main-content {
    margin-right: 0;
    padding: 15px;
  }

  .dashboard-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .dashboard-header h1 {
    font-size: 20px;
  }
}
</style>