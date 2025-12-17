<template>
  <div class="admin-layout">
    <button class="hamburger-menu" @click="sidebarOpen = !sidebarOpen" :class="{ active: sidebarOpen }">
      <span></span>
      <span></span>
      <span></span>
    </button>
    
    <aside class="admin-sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <h2>🎛️ مدیریت</h2>
        <button class="close-sidebar" @click="sidebarOpen = false">✕</button>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/admin/dashboard" class="nav-item" :class="{ active: isActive('dashboard') }" @click="closeSidebar">
          📊 داشبورد
        </router-link>
        <router-link to="/admin/reports" class="nav-item" :class="{ active: isActive('reports') }" @click="closeSidebar">
          📈 گزارش‌ها
        </router-link>
        <router-link to="/admin/articles" class="nav-item" :class="{ active: isActive('articles') }" @click="closeSidebar">
          📝 مقالات
        </router-link>
        <router-link to="/admin/gallery" class="nav-item" :class="{ active: isActive('gallery') }" @click="closeSidebar">
          🎨 گالری
        </router-link>
        <router-link to="/admin/testimonials" class="nav-item" :class="{ active: isActive('testimonials') }" @click="closeSidebar">
          ⭐ دیدگاه های برتر
        </router-link>
        <router-link to="/admin/contacts" class="nav-item" :class="{ active: isActive('contacts') }" @click="closeSidebar">
          📧 پیام‌ها
        </router-link>
        <router-link to="/admin/users" class="nav-item" :class="{ active: isActive('users') }" @click="closeSidebar">
          👤 کاربران
        </router-link>
        <router-link to="/admin/sliders" class="nav-item" :class="{ active: isActive('sliders') }" @click="closeSidebar">
          🎬 اسلایدرها
        </router-link>
        <router-link to="/admin/certificates" class="nav-item" :class="{ active: isActive('certificates') }" @click="closeSidebar">
          📜 گواهینامه‌ها
        </router-link>
        <router-link to="/admin/comments" class="nav-item" :class="{ active: isActive('comments') }" @click="closeSidebar">
          💬 نظرات
        </router-link>
        <router-link to="/admin/videos" class="nav-item" :class="{ active: isActive('videos') }" @click="closeSidebar">
          🎥 ویدیوها
        </router-link>
        <router-link to="/admin/services" class="nav-item" :class="{ active: isActive('services') }" @click="closeSidebar">
          🎯 خدمات
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
const sidebarOpen = ref(false)

const pageTitle = computed(() => {
  const titles = {
    'AdminDashboard': '📊 داشبورد',
    'AdminReports': '📈 گزارش‌ها',
    'AdminArticles': '📝 مقالات',
    'AdminGallery': '🎨 گالری',
    'AdminTestimonials': '⭐ نظرات مشتریان',
    'AdminContacts': '📧 پیام‌های تماس',
    'AdminUsers': '👤 کاربران',
    'AdminSliders': '🎬 اسلایدرها',
    'AdminCertificates': '📜 گواهینامه‌ها و استانداردها',
    'AdminComments': '💬 نظرات و امتیازات',
    'AdminVideos': '🎥 ویدیوها'
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

const closeSidebar = () => {
  sidebarOpen.value = false
}

onMounted(() => {
  const user = localStorage.getItem('admin_user')
  if (user) {
    currentUser.value = JSON.parse(user)
  }
})
</script>

<style scoped>
.admin-layout { display: flex; height: 100vh; background: var(--admin-bg); color: var(--admin-text); }

.hamburger-menu { display: none; position: fixed; top: 1rem; left: 1rem; z-index: 1001; background: linear-gradient(135deg, var(--admin-primary-start), var(--admin-primary-end)); border: none; padding: 0.75rem; border-radius: 0.75rem; cursor: pointer; flex-direction: column; gap: 0.4rem; box-shadow: 0 10px 28px rgba(102,126,234,0.25); }
.hamburger-menu span { width: 22px; height: 3px; background: #fff; border-radius: 2px; transition: all 0.3s ease; }
.hamburger-menu.active span:nth-child(1) { transform: rotate(45deg) translate(6px, 6px); }
.hamburger-menu.active span:nth-child(2) { opacity: 0; }
.hamburger-menu.active span:nth-child(3) { transform: rotate(-45deg) translate(6px, -6px); }

.close-sidebar { display: none; background: none; border: none; color: #fff; font-size: 1.5rem; cursor: pointer; padding: 0.5rem; margin-right: auto; }

.admin-sidebar { width: 260px; background: linear-gradient(180deg, rgba(15,23,42,0.95) 0%, rgba(49,46,129,0.9) 100%); color: #fff; overflow-y: auto; box-shadow: 4px 0 20px rgba(0,0,0,0.25); backdrop-filter: blur(10px); position: relative; }
.sidebar-header { padding: 1.75rem 1.5rem 1.25rem; border-bottom: 1px solid rgba(255,255,255,0.08); }
.sidebar-header h2 { font-size: 1.4rem; margin: 0; letter-spacing: 0.01em; }

.sidebar-nav { padding: 0.75rem 0; display: flex; flex-direction: column; gap: 0.25rem; }
.nav-item { padding: 0.85rem 1.5rem; color: rgba(255,255,255,0.82); text-decoration: none; transition: all 0.25s ease; border-right: 4px solid transparent; font-size: 0.95rem; font-weight: 600; border-radius: 10px; margin: 0 0.75rem; }
.nav-item:hover { background: rgba(255,255,255,0.08); color: #fff; transform: translateX(-4px); box-shadow: 0 10px 24px rgba(0,0,0,0.18); }
.nav-item.active { background: rgba(255,255,255,0.12); color: #fff; border-right-color: #fff; box-shadow: inset -3px 0 0 rgba(255,255,255,0.4), 0 10px 26px rgba(0,0,0,0.2); }

.sidebar-footer { padding: 1.25rem 1.5rem 1.5rem; border-top: 1px solid rgba(255,255,255,0.08); margin-top: auto; }
.logout-button { width: 100%; padding: 0.75rem; background: linear-gradient(135deg, #f5576c, #f093fb); color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: 700; transition: transform 0.2s ease, box-shadow 0.2s ease; }
.logout-button:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(245,87,108,0.35); }

.admin-main { flex: 1; display: flex; flex-direction: column; overflow: hidden; background: radial-gradient(circle at 20% 20%, rgba(102,126,234,0.08), transparent 30%), radial-gradient(circle at 80% 0%, rgba(245,87,108,0.08), transparent 28%), var(--admin-bg-2); }

.admin-header { background: rgba(255,255,255,0.9); backdrop-filter: blur(12px); padding: 1.25rem 1.75rem; box-shadow: 0 12px 30px rgba(15,23,42,0.08); display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(226,232,240,0.8); position: sticky; top: 0; z-index: 5; }
.admin-header h1 { margin: 0; font-size: 1.5rem; background: linear-gradient(135deg, var(--admin-primary-start), var(--admin-primary-end)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 800; letter-spacing: 0.01em; }
.admin-user { display: flex; align-items: center; gap: 1rem; color: var(--admin-muted); font-weight: 600; }
.user-logout { padding: 0.55rem 1rem; background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.08)); color: #0f172a; border: 1px solid rgba(102,126,234,0.25); border-radius: 10px; cursor: pointer; font-size: 0.9rem; font-weight: 700; transition: transform 0.2s ease, box-shadow 0.2s ease; backdrop-filter: blur(6px); }
.user-logout:hover { transform: translateY(-2px); box-shadow: 0 10px 22px rgba(102,126,234,0.2); }

.admin-content { flex: 1; overflow-y: auto; padding: 1.5rem 1.75rem 2rem; }
.admin-content::-webkit-scrollbar { width: 8px; }
.admin-content::-webkit-scrollbar-thumb { background: linear-gradient(135deg, var(--admin-primary-start), var(--admin-primary-end)); border-radius: 999px; }

@media (max-width: 1024px) {
  .hamburger-menu { display: flex; }
  .admin-layout { flex-direction: column; }
  .admin-sidebar { position: fixed; left: 0; top: 0; width: 78%; max-width: 280px; height: 100vh; z-index: 1000; transform: translateX(-100%); transition: transform 0.3s ease; box-shadow: 4px 0 24px rgba(0,0,0,0.35); }
  .admin-sidebar.open { transform: translateX(0); }
  .sidebar-header { display: flex; justify-content: space-between; align-items: center; }
  .close-sidebar { display: block; }
  .admin-header { flex-direction: column; align-items: flex-start; gap: 0.8rem; padding-left: 4rem; }
  .admin-header h1 { font-size: 1.25rem; }
  .admin-user { width: 100%; justify-content: space-between; }
  .admin-content { padding: 1.25rem 1.25rem 1.75rem; }
}

@media (max-width: 540px) {
  .hamburger-menu { top: 0.75rem; left: 0.75rem; }
  .admin-header { padding: 1rem 1.25rem 1rem 4rem; }
  .admin-header h1 { font-size: 1.05rem; }
  .admin-user { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
  .user-logout { width: 100%; text-align: center; }
  .nav-item { padding: 0.8rem 1.25rem; font-size: 0.92rem; }
  .sidebar-header h2 { font-size: 1.2rem; }
  .admin-content { padding: 1rem; }
}
</style>
