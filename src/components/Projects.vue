<template>
  <section class="projects-section" id="projects">
    <h2 class="section-title animate-on-scroll">پروژه‌های ما</h2>
    <div class="projects-grid">
      <div class="project-card animate-on-scroll" v-for="(project, index) in projects" :key="project.id">
        <div class="project-image">
          <img :src="project.image_url || 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 250%27%3E%3Crect fill=%27%23ddd%27 width=%27300%27 height=%27250%27/%3E%3C/svg%3E'" :alt="project.title_fa || project.title_en">
        </div>
        <div class="project-content">
          <h3>{{ project.title_fa || project.title_en }}</h3>
          <p>{{ project.description_fa || project.description_en }}</p>
          <div class="project-actions">
            <a href="#" @click.prevent="navigateTo(`/project/${project.id}`)" class="btn-link">مشاهده پروژه</a>
            <a v-if="project.archive_url" :href="project.archive_url" target="_blank" rel="noopener noreferrer" class="btn-link secondary">دانلود آرشیو</a>
          </div>
        </div>
      </div>
    </div>
    
    <!-- View All Projects Button -->
    <div class="view-all-button">
      <a href="#" @click.prevent="navigateTo('/projects-archive')" class="btn-view-all">مشاهده تمام پروژه‌ها</a>
    </div>
  </section>
</template>

<script>
import { projectService } from '../services/api';

export default {
  name: 'Projects',
  inject: ['navigateTo'],
  data() {
    return {
      projects: [],
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchProjects();
    // Ensure elements are visible when component mounts
    this.$nextTick(() => {
      setTimeout(() => {
        const elements = this.$el.querySelectorAll('.animate-on-scroll');
        elements.forEach(el => el.classList.add('in-view'));
      }, 50);
    });
  },
  methods: {
    async fetchProjects() {
      this.loading = true;
      this.error = null;
      try {
        const response = await projectService.getAll({ is_featured: true });
        this.projects = response.data.slice(0, 6);
      } catch (err) {
        this.error = 'خطا در بارگذاری پروژه‌ها';
        console.error('Error fetching projects:', err);
        this.projects = [];
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.projects-section {
  padding: 40px 50px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-title {
  font-size: 32px;
  font-weight: bold;
  text-align: right;
  margin-bottom: 15px;
  color: #1a1a1a;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  width: 100%;
  max-width: 1200px;
  margin-top: 25px;
}

.project-card {
  background: #ffffff;
  cursor: pointer;
  transition: all 0.3s ease-out;
  text-align: right;
  overflow: hidden;
}

.project-card:hover {
  transform: translateY(-4px);
}

.project-image {
  width: 100%;
  height: 250px;
  overflow: hidden;
  background: #f5f5f5;
}

.project-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease-out;
}

.project-card:hover .project-image img {
  transform: scale(1.05);
}

.project-content {
  padding: 15px;
}

.project-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #1a1a1a;
  word-wrap: break-word;
  word-break: break-word;
}

.project-card p {
  font-size: 14px;
  line-height: 1.6;
  color: #666666;
  margin-bottom: 20px;
  min-height: 60px;
}

.project-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-link {
  display: inline-block;
  padding: 10px 15px;
  background: transparent;
  color: #666;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 2px;
}

.btn-link:hover {
  background: #f5f5f5;
  border-color: #999;
  transform: scale(1.02);
}

.btn-link.secondary {
  background: transparent;
  color: #666;
  border: 1px solid #ddd;
}

.btn-link.secondary:hover {
  background: #f5f5f5;
  border-color: #999;
}

/* View All Button */
.view-all-button {
  text-align: center;
  margin-top: 50px;
  margin-bottom: 20px;
}

.btn-view-all {
  display: inline-block;
  padding: 14px 40px;
  background: transparent;
  color: #666;
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  border: 1px solid #999;
  border-radius: 2px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.btn-view-all:hover {
  background: #f5f5f5;
  color: #333;
  transform: scale(1.02);
}

.btn-view-all:active {
  transform: scale(0.98);
}

/* Animations */
.animate-on-scroll {
  opacity: 0;
  animation: none;
}

.animate-on-scroll.in-view {
  animation: slideUp 0.6s ease-out forwards;
}

.animate-on-scroll:nth-child(2).in-view {
  animation: slideUp 0.6s ease-out 0.1s forwards;
}

.animate-on-scroll:nth-child(3).in-view {
  animation: slideUp 0.6s ease-out 0.2s forwards;
}

.animate-on-scroll:nth-child(4).in-view {
  animation: slideUp 0.6s ease-out 0.3s forwards;
}

.animate-on-scroll:nth-child(5).in-view {
  animation: slideUp 0.6s ease-out 0.4s forwards;
}

.animate-on-scroll:nth-child(6).in-view {
  animation: slideUp 0.6s ease-out 0.5s forwards;
}

.animate-on-scroll:nth-child(n+7).in-view {
  animation: slideUp 0.6s ease-out 0.6s forwards;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Loading state */
.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

/* Error state */
.error {
  text-align: center;
  padding: 40px;
  color: #d32f2f;
  background: #ffebee;
  border-radius: 2px;
}

/* Responsive */
@media (max-width: 1024px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .projects-section {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 30px;
  }

  .projects-section {
    padding: 30px 20px;
  }

  .section-title {
    font-size: 24px;
  }

  .project-card {
    padding: 0;
  }

  .project-image {
    height: 200px;
  }

  .project-content {
    padding: 20px;
  }

  .project-card h3 {
    font-size: 16px;
    margin-bottom: 10px;
  }

  .project-card p {
    font-size: 13px;
    min-height: auto;
  }
}
</style>
