<template>
  <div class="admin-layout">
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <h2>🎛️ مدیریت</h2>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/admin/dashboard" class="nav-item" :class="{ active: isActive('dashboard') }">
          📊 داشبورد
        </router-link>
        <router-link to="/admin/articles" class="nav-item" :class="{ active: isActive('articles') }">
          📝 مقالات
        </router-link>
        <router-link to="/admin/gallery" class="nav-item" :class="{ active: isActive('gallery') }">
          🎨 گالری
        </router-link>
        <router-link to="/admin/testimonials" class="nav-item" :class="{ active: isActive('testimonials') }">
          ⭐ نظرات
        </router-link>
        <router-link to="/admin/contacts" class="nav-item" :class="{ active: isActive('contacts') }">
          📧 پیام‌ها
        </router-link>
        <router-link to="/admin/sliders" class="nav-item" :class="{ active: isActive('sliders') }">
          🎬 اسلایدرها
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <button @click="handleLogout" class="logout-button">
          🚪 خروج
        </button>
      </div>
    </aside>

    <main class="admin-main">
      <header class="admin-header">
        <h1>{{ pageTitle }}</h1>
        <div class="admin-user">
          <span>{{ currentUser?.full_name || 'ادمین' }}</span>
          <button @click="handleLogout" class="user-logout">خروج</button>
        </div>
      </header>
      <div class="admin-content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const currentUser = ref(null)

const pageTitle = computed(() => {
  const titles = {
    'AdminDashboard': '📊 داشبورد',
    'AdminArticles': '📝 مقالات',
    'AdminGallery': '🎨 گالری',
    'AdminTestimonials': '⭐ نظرات',
    'AdminContacts': '📧 پیام‌های تماس',
    'AdminSliders': '🎬 اسلایدرها'
  }
  return titles[route.name] || 'پنل مدیریت'
})

const isActive = (page) => {
  return route.path.includes(page)
}

const handleLogout = () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  router.push('/admin/login')
}

onMounted(() => {
  const user = localStorage.getItem('admin_user')
  if (user) {
    currentUser.value = JSON.parse(user)
  }
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.admin-sidebar {
  width: 250px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  color: white;
  overflow-y: auto;
  box-shadow: 4px 0 20px rgba(102, 126, 234, 0.3);
}

.sidebar-header {
  padding: 2rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  font-size: 1.5rem;
  margin: 0;
}

.sidebar-nav {
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
}

.nav-item {
  padding: 0.875rem 1.5rem;
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
  font-size: 0.95rem;
  font-weight: 500;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  padding-right: 2rem;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-left-color: white;
  box-shadow: inset -4px 0 8px rgba(0, 0, 0, 0.1);
}

.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
}

.logout-button {
  width: 100%;
  padding: 0.75rem;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.logout-button:hover {
  background: #c53030;
}

.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.admin-header {
  background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
  padding: 1.5rem 2rem;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e2e8f0;
}

.admin-header h1 {
  margin: 0;
  font-size: 1.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.admin-user {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  color: #2d3748;
  font-weight: 500;
}

.user-logout {
  padding: 0.6rem 1.2rem;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(245, 87, 108, 0.3);
}

.user-logout:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(245, 87, 108, 0.4);
}

.admin-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.admin-content::-webkit-scrollbar {
  width: 8px;
}

.admin-content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
}

.admin-content::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
}

.admin-content::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

@media (max-width: 768px) {
  .admin-layout {
    flex-direction: column;
  }

  .admin-sidebar {
    width: 100%;
    height: auto;
    max-height: auto;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
  }

  .sidebar-nav {
    flex-direction: row;
    overflow-x: auto;
    padding: 0.5rem 0;
  }

  .nav-item {
    white-space: nowrap;
    border-left: none;
    border-bottom: 3px solid transparent;
    padding: 0.75rem 1rem;
  }

  .nav-item.active {
    border-left: none;
    border-bottom: 3px solid white;
    box-shadow: none;
  }

  .admin-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .admin-header h1 {
    font-size: 1.25rem;
  }

  .admin-user {
    width: 100%;
    justify-content: space-between;
  }

  .admin-content {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .admin-header h1 {
    font-size: 1rem;
  }

  .admin-content {
    padding: 0.5rem;
  }

  .nav-item {
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
  }

  .sidebar-header h2 {
    font-size: 1.25rem;
  }
}
</style>
