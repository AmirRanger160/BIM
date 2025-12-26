<template>
  <div class="dashboard-stats">
    <div v-if="loading" class="stats-loading">
      <div class="spinner"></div>
      <p>در حال بارگذاری آمار...</p>
    </div>
    <div v-else class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-content">
          <h3>{{ statsData.articles || 0 }}</h3>
          <p>مقالات</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🏗️</div>
        <div class="stat-content">
          <h3>{{ statsData.projects || 0 }}</h3>
          <p>پروژه‌ها</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div class="stat-content">
          <h3>{{ statsData.contacts || 0 }}</h3>
          <p>تماس‌ها</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>{{ statsData.team || 0 }}</h3>
          <p>اعضای تیم</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from '../composables/useToast';
import { 
  adminArticleService, 
  adminProjectService, 
  adminContactService,
  adminTeamService
} from '../services/api';

export default {
  name: 'DashboardStats',
  props: {
    stats: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      statsData: {
        articles: 0,
        projects: 0,
        contacts: 0,
        team: 0
      },
      loading: false
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  mounted() {
    this.loadStats();
  },
  methods: {
    async loadStats() {
      this.loading = true;
      try {
        // Load counts from API
        const [articles, projects, contacts, team] = await Promise.all([
          adminArticleService.getAll({ limit: 1 }).catch(() => ({ data: [] })),
          adminProjectService.getAll({ limit: 1 }).catch(() => ({ data: [] })),
          adminContactService.getAll({ limit: 1 }).catch(() => ({ data: [] })),
          adminTeamService.getAll({ limit: 1 }).catch(() => ({ data: [] }))
        ]);

        // Extract counts from responses
        this.statsData = {
          articles: articles.data?.total || articles.data?.length || 0,
          projects: projects.data?.total || projects.data?.length || 0,
          contacts: contacts.data?.total || contacts.data?.length || 0,
          team: team.data?.total || team.data?.length || 0
        };

        // If props provide stats, use those
        if (this.stats) {
          this.statsData = { ...this.statsData, ...this.stats };
        }
      } catch (error) {
        console.error('Failed to load dashboard stats:', error);
        this.toast.error('خطا در بارگذاری آمار');
        // Use prop stats if API fails
        if (this.stats) {
          this.statsData = this.stats;
        }
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.dashboard-stats {
  margin-bottom: 30px;
}

.stats-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1abc9c;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.stats-loading p {
  color: #666;
  font-size: 14px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
  border-left: 4px solid #1abc9c;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  font-size: 32px;
  opacity: 0.8;
}

.stat-content h3 {
  margin: 0 0 5px 0;
  font-size: 28px;
  font-weight: bold;
  color: #1abc9c;
}

.stat-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 15px;
  }

  .stat-content h3 {
    font-size: 24px;
  }
}
</style>