<template>
  <div class="dashboard">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-info">
          <h3>مقالات</h3>
          <p class="stat-number">{{ stats.articles }}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">🎨</div>
        <div class="stat-info">
          <h3>گالری</h3>
          <p class="stat-number">{{ stats.gallery }}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">⭐</div>
        <div class="stat-info">
          <h3>نظرات</h3>
          <p class="stat-number">{{ stats.testimonials }}</p>
        </div>
      </div>

      <div class="stat-card alert">
        <div class="stat-icon">📧</div>
        <div class="stat-info">
          <h3>پیام‌های خوانده‌نشده</h3>
          <p class="stat-number">{{ stats.unread_contacts }}</p>
        </div>
      </div>

      <div class="stat-card alert">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <h3>نظرات در انتظار تایید</h3>
          <p class="stat-number">{{ stats.pending_testimonials }}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📞</div>
        <div class="stat-info">
          <h3>کل پیام‌ها</h3>
          <p class="stat-number">{{ stats.contacts }}</p>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>عملیات سریع</h2>
      <div class="actions-grid">
        <router-link to="/admin/articles" class="action-button">
          ➕ افزودن مقاله
        </router-link>
        <router-link to="/admin/gallery" class="action-button">
          ➕ افزودن به گالری
        </router-link>
        <router-link to="/admin/testimonials" class="action-button">
          ➕ افزودن نظر
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminService } from '../api/services'

const stats = ref({
  articles: 0,
  gallery: 0,
  testimonials: 0,
  contacts: 0,
  unread_contacts: 0,
  pending_testimonials: 0
})

onMounted(async () => {
  try {
    stats.value = await adminService.getDashboardStats()
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error)
  }
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.stat-card.alert {
  border-color: #fed7d7;
  background: #fff5f5;
}

.stat-icon {
  font-size: 2.5rem;
  line-height: 1;
}

.stat-info h3 {
  margin: 0;
  font-size: 0.95rem;
  color: #718096;
  font-weight: 500;
}

.stat-number {
  margin: 0.5rem 0 0 0;
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
}

.stat-card.alert .stat-number {
  color: #e53e3e;
}

.quick-actions {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.quick-actions h2 {
  margin-top: 0;
  color: #2d3748;
  font-size: 1.25rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-button {
  padding: 1.25rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 10px;
  text-align: center;
  font-weight: 600;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
