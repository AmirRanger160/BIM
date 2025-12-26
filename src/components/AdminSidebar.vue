<template>
  <div class="admin-sidebar-wrapper">
    <!-- Sidebar Toggle Button (Mobile) -->
    <button
      class="sidebar-toggle"
      @click="toggleSidebar"
      :class="{ active: isOpen }"
      aria-label="تغییر وضعیت منو"
    >
      <span class="toggle-icon">☰</span>
    </button>

    <!-- Overlay for Mobile -->
    <div
      v-if="isOpen && isMobile"
      class="sidebar-overlay"
      @click="closeSidebar"
    ></div>

    <!-- Sidebar -->
    <div
      class="admin-sidebar"
      :class="{ open: isOpen, collapsed: !isOpen }"
    >
      <!-- Header -->
      <div class="sidebar-header">
        <div class="header-content">
          <div class="logo">
            <span class="logo-icon">🎯</span>
            <span v-if="isOpen" class="logo-text">پنل مدیریت</span>
          </div>
          <button
            class="collapse-btn"
            @click="toggleSidebar"
            :aria-label="isOpen ? 'بستن منو' : 'باز کردن منو'"
          >
            <span class="collapse-icon">{{ isOpen ? '◁' : '▷' }}</span>
          </button>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="sidebar-nav">
        <ul class="nav-list">
          <li class="nav-item">
            <a
              href="#"
              class="nav-link"
              @click.prevent="handleNavigate('/admin')"
              :class="{ active: isActive('/admin') }"
            >
              <span class="nav-icon">📊</span>
              <span v-if="isOpen" class="nav-text">داشبورد</span>
            </a>
          </li>
          <li class="nav-item">
            <a
              href="#"
              class="nav-link"
              @click.prevent="handleNavigate('/admin/articles')"
              :class="{ active: isActive('/admin/articles') }"
            >
              <span class="nav-icon">📝</span>
              <span v-if="isOpen" class="nav-text">مقالات</span>
            </a>
          </li>
          <li class="nav-item">
            <a
              href="#"
              class="nav-link"
              @click.prevent="handleNavigate('/admin/projects')"
              :class="{ active: isActive('/admin/projects') }"
            >
              <span class="nav-icon">🏗️</span>
              <span v-if="isOpen" class="nav-text">پروژه‌ها</span>
            </a>
          </li>
          <li class="nav-item">
            <a
              href="#"
              class="nav-link"
              @click.prevent="handleNavigate('/admin/services')"
              :class="{ active: isActive('/admin/services') }"
            >
              <span class="nav-icon">🛠️</span>
              <span v-if="isOpen" class="nav-text">خدمات</span>
            </a>
          </li>
          <li class="nav-item">
            <a
              href="#"
              class="nav-link"
              @click.prevent="handleNavigate('/admin/team')"
              :class="{ active: isActive('/admin/team') }"
            >
              <span class="nav-icon">👥</span>
              <span v-if="isOpen" class="nav-text">تیم</span>
            </a>
          </li>
          <li class="nav-item">
            <a
              href="#"
              class="nav-link"
              @click.prevent="handleNavigate('/admin/certificates')"
              :class="{ active: isActive('/admin/certificates') }"
            >
              <span class="nav-icon">🏆</span>
              <span v-if="isOpen" class="nav-text">گواهینامه‌ها</span>
            </a>
          </li>
          <li class="nav-item">
            <a
              href="#"
              class="nav-link"
              @click.prevent="handleNavigate('/admin/licenses')"
              :class="{ active: isActive('/admin/licenses') }"
            >
              <span class="nav-icon">📄</span>
              <span v-if="isOpen" class="nav-text">مجوزها</span>
            </a>
          </li>
          <li class="nav-item">
            <a
              href="#"
              class="nav-link"
              @click.prevent="handleNavigate('/admin/contacts')"
              :class="{ active: isActive('/admin/contacts') }"
            >
              <span class="nav-icon">💬</span>
              <span v-if="isOpen" class="nav-text">تماس‌ها</span>
            </a>
          </li>
          <li class="nav-item">
            <a
              href="#"
              class="nav-link"
              @click.prevent="handleNavigate('/admin/users')"
              :class="{ active: isActive('/admin/users') }"
            >
              <span class="nav-icon">👤</span>
              <span v-if="isOpen" class="nav-text">کاربران</span>
            </a>
          </li>
          <li class="nav-item">
            <a
              href="#"
              class="nav-link"
              @click.prevent="handleNavigate('/admin/settings')"
              :class="{ active: isActive('/admin/settings') }"
            >
              <span class="nav-icon">⚙️</span>
              <span v-if="isOpen" class="nav-text">تنظیمات</span>
            </a>
          </li>
        </ul>
      </nav>

      <!-- Footer -->
      <div class="sidebar-footer" v-if="isOpen">
        <div class="user-info">
          <span class="user-avatar">👨‍💼</span>
          <span class="user-name">مدیر سیستم</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminSidebar',
  data() {
    return {
      isOpen: true,
      isMobile: false,
      currentRoute: window.location.pathname
    }
  },
  mounted() {
    this.checkScreenSize();
    window.addEventListener('resize', this.checkScreenSize);

    // Close sidebar on mobile by default
    if (this.isMobile) {
      this.isOpen = false;
    }

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', this.handleOutsideClick);

    // Watch for route changes
    this.watchRoute();

    // Emit initial state
    this.emitStateChange();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkScreenSize);
    document.removeEventListener('click', this.handleOutsideClick);
  },
  methods: {
    checkScreenSize() {
      const wasMobile = this.isMobile;
      this.isMobile = window.innerWidth <= 768;
      if (this.isMobile && this.isOpen) {
        this.isOpen = false;
      }
      // Emit state change if mobile status changed
      if (wasMobile !== this.isMobile) {
        this.emitStateChange();
      }
    },
    toggleSidebar() {
      this.isOpen = !this.isOpen;
      this.emitStateChange();
    },
    closeSidebar() {
      if (this.isMobile) {
        this.isOpen = false;
        this.emitStateChange();
      }
    },
    emitStateChange() {
      this.$emit('sidebar-state-change', {
        isOpen: this.isOpen,
        isMobile: this.isMobile
      });
    },
    handleNavigate(route) {
      this.currentRoute = route; // Update reactive route
      this.$emit('navigate', route);
      // Close sidebar on mobile after navigation
      if (this.isMobile) {
        this.isOpen = false;
      }
    },
    handleOutsideClick(event) {
      const sidebar = this.$el.querySelector('.admin-sidebar');
      const toggle = this.$el.querySelector('.sidebar-toggle');

      if (this.isMobile && this.isOpen &&
          !sidebar.contains(event.target) &&
          !toggle.contains(event.target)) {
        this.closeSidebar();
      }
    },
    watchRoute() {
      // Watch for URL changes every 100ms to update active state
      setInterval(() => {
        const currentPath = window.location.pathname;
        if (currentPath !== this.currentRoute) {
          this.currentRoute = currentPath;
        }
      }, 100);
    },
    isActive(route) {
      return this.currentRoute === route;
    }
  }
}
</script>

<style scoped>
.admin-sidebar-wrapper {
  position: relative;
}

/* Mobile Toggle Button */
.sidebar-toggle {
  display: none;
  position: fixed;
  top: 15px;
  right: 15px;
  z-index: 101;
  background: #1abc9c;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(26, 188, 156, 0.3);
  transition: all 0.3s ease;
}

.sidebar-toggle:hover {
  background: #16a085;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(26, 188, 156, 0.4);
}

.sidebar-toggle.active {
  background: #e74c3c;
}

.toggle-icon {
  font-size: 16px;
  font-weight: bold;
}

/* Mobile Overlay */
.sidebar-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
  backdrop-filter: blur(2px);
}

/* Main Sidebar */
.admin-sidebar {
  position: fixed;
  right: 0;
  top: 0;
  width: 280px;
  height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
  z-index: 100;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-y: auto;
  border-left: 1px solid rgba(26, 188, 156, 0.1);
}

.admin-sidebar.collapsed {
  width: 70px;
  overflow: visible;
}

.admin-sidebar.open {
  transform: translateX(0);
}

/* Header */
.sidebar-header {
  padding: 0;
  background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%);
  color: white;
  border-bottom: none;
  position: relative;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  min-height: 70px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 24px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  white-space: nowrap;
  transition: opacity 0.3s ease;
}

.collapse-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.collapse-icon {
  font-size: 16px;
  font-weight: bold;
}

/* Navigation */
.sidebar-nav {
  padding: 20px 0;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: #666;
  text-decoration: none;
  transition: background-color 0.2s ease, color 0.2s ease;
  border-radius: 0 25px 25px 0;
  margin-right: 8px;
  margin-left: 8px;
  cursor: pointer;
}

.nav-link:hover {
  background: rgba(26, 188, 156, 0.1);
  color: #1abc9c;
}

.nav-link.active {
  background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%);
  color: white;
}

.nav-icon {
  font-size: 20px;
  margin-left: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  transition: transform 0.3s ease;
}

.nav-link:hover .nav-icon {
  transform: scale(1.1);
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  transition: opacity 0.3s ease;
}

/* Footer */
.sidebar-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  font-size: 24px;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

/* Collapsed State */
.admin-sidebar.collapsed .logo-text,
.admin-sidebar.collapsed .nav-text,
.admin-sidebar.collapsed .user-name,
.admin-sidebar.collapsed .sidebar-footer {
  opacity: 0;
  pointer-events: none;
}

.admin-sidebar.collapsed .header-content {
  justify-content: center;
}

.admin-sidebar.collapsed .nav-link {
  justify-content: center;
  padding: 12px;
}

.admin-sidebar.collapsed .nav-link:hover {
  transform: none;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .sidebar-toggle {
    display: block;
  }

  .sidebar-overlay {
    display: block;
  }

  .admin-sidebar {
    transform: translateX(100%);
    width: 280px;
  }

  .admin-sidebar.open {
    transform: translateX(0);
  }

  .admin-sidebar.collapsed {
    width: 280px; /* Don't collapse on mobile */
  }

  .admin-sidebar.collapsed .logo-text,
  .admin-sidebar.collapsed .nav-text,
  .admin-sidebar.collapsed .user-name,
  .admin-sidebar.collapsed .sidebar-footer {
    opacity: 1;
    pointer-events: auto;
  }

  .admin-sidebar.collapsed .header-content {
    justify-content: space-between;
  }

  .admin-sidebar.collapsed .nav-link {
    justify-content: flex-start;
    padding: 12px 20px;
  }
}

/* RTL Adjustments */
[dir="rtl"] .nav-link::before {
  right: auto;
  left: -20px;
  border-radius: 0 2px 2px 0;
}

[dir="rtl"] .nav-link:hover {
  transform: translateX(4px);
}

/* Subtle hover animation only */
.nav-link {
  transition: all 0.2s ease;
}

/* Scrollbar Styling */
.admin-sidebar::-webkit-scrollbar {
  width: 6px;
}

.admin-sidebar::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
}

.admin-sidebar::-webkit-scrollbar-thumb {
  background: rgba(26, 188, 156, 0.3);
  border-radius: 3px;
}

.admin-sidebar::-webkit-scrollbar-thumb:hover {
  background: rgba(26, 188, 156, 0.5);
}
</style>