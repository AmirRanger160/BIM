<template>
  <section class="projects-archive" id="projects-archive">
    <div class="container">
      <h1 class="page-title animate-on-scroll">آرشیو پروژه‌های ما</h1>
      
      <!-- Filters -->
      <div class="filters animate-on-scroll">
        <div class="filter-group">
          <label for="category-select">دسته‌بندی:</label>
          <select v-model="selectedCategory" id="category-select" @change="filterProjects">
            <option value="">تمام دسته‌بندی‌ها</option>
            <option value="BIM">BIM</option>
            <option value="Surveying">نقشه‌برداری</option>
          </select>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>درحال بارگذاری پروژه‌ها...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error">
        <p>{{ error }}</p>
      </div>

      <!-- Projects Grid -->
      <div v-else-if="filteredProjects.length > 0" class="projects-grid">
        <div v-for="project in filteredProjects" :key="project.id" class="project-card animate-on-scroll">
          <div class="project-image">
            <img :src="project.image_url || 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 400 300%27%3E%3Crect fill=%27%23ddd%27 width=%27400%27 height=%27300%27/%3E%3C/svg%3E'" :alt="project.title_fa || project.title_en">
            <div class="project-overlay">
              <a href="#" @click.prevent="navigateTo(`/project/${project.id}`)" class="btn-view">مشاهده پروژه</a>
            </div>
          </div>
          <div class="project-info">
            <span class="category" v-if="project.category">{{ project.category }}</span>
            <h3>{{ project.title_fa || project.title_en }}</h3>
            <p>{{ project.description_fa || project.description_en }}</p>
          </div>
        </div>
      </div>

      <!-- No Projects -->
      <div v-else class="no-projects">
        <p>هیچ پروژه‌ای یافت نشد.</p>
      </div>
    </div>
  </section>
</template>

<script>
import { projectService } from '../services/api';

export default {
  name: 'ProjectsArchive',
  inject: ['navigateTo'],
  data() {
    return {
      projects: [],
      filteredProjects: [],
      loading: false,
      error: null,
      selectedCategory: ''
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
        const response = await projectService.getAll();
        this.projects = response.data;
        this.filterProjects();
      } catch (err) {
        this.error = 'خطا در بارگذاری پروژه‌ها';
        console.error('Error fetching projects:', err);
      } finally {
        this.loading = false;
      }
    },
    filterProjects() {
      if (this.selectedCategory) {
        this.filteredProjects = this.projects.filter(p => p.category === this.selectedCategory);
      } else {
        this.filteredProjects = this.projects;
      }
    }
  }
}
</script>

<style scoped>
.projects-archive {
  padding: 60px 50px;
  background: #ffffff;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 36px;
  font-weight: bold;
  text-align: right;
  margin-bottom: 40px;
  color: #1a1a1a;
}

/* Filters */
.filters {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 20px;
  margin-bottom: 50px;
  padding: 20px 0;
  text-align: right;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-group label {
  font-weight: 600;
  color: #333;
  font-size: 13px;
}

.filter-group select {
  padding: 8px 10px;
  border: none;
  border-bottom: 1px solid #ddd;
  font-size: 13px;
  direction: rtl;
  text-align: right;
  background: transparent;
  min-width: 150px;
}

.filter-group select:focus {
  outline: none;
  border-bottom-color: #1abc9c;
}

/* Projects Grid */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-bottom: 50px;
}

.project-card {
  background: #ffffff;
  overflow: hidden;
  transition: all 0.3s ease-out;
  cursor: pointer;
}

.project-card:hover {
  transform: translateY(-4px);
}

.project-image {
  position: relative;
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
  transform: scale(1.1);
}

.project-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease-out;
}

.project-card:hover .project-overlay {
  opacity: 1;
}

.btn-view {
  padding: 12px 24px;
  background: #1abc9c;
  color: white;
  text-decoration: none;
  font-weight: 600;
  border-radius: 2px;
  transition: all 0.3s ease-out;
}

.btn-view:hover {
  background: #16a085;
  transform: scale(1.05);
}

.project-info {
  padding: 25px;
  text-align: right;
}

.category {
  display: inline-block;
  background: #1abc9c;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 10px;
}

.project-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #1a1a1a;
  line-height: 1.4;
}

.project-card p {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}

/* Loading & Error States */
.loading, .error, .no-projects {
  text-align: center;
  padding: 60px 20px;
  font-size: 16px;
}

.loading {
  color: #666;
}

.error {
  background: #ffebee;
  color: #d32f2f;
  border-radius: 2px;
}

.no-projects {
  color: #999;
}

/* Animations */
.animate-on-scroll {
  opacity: 0;
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

/* Responsive */
@media (max-width: 1024px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .projects-archive {
    padding: 30px 20px;
  }

  .page-title {
    font-size: 24px;
    margin-bottom: 30px;
  }

  .filters {
    flex-direction: column;
    gap: 15px;
    padding: 20px;
  }

  .filter-group {
    min-width: auto;
    width: 100%;
  }

  .projects-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .project-image {
    height: 200px;
  }

  .project-info {
    padding: 20px;
  }

  .project-card h3 {
    font-size: 16px;
  }

  .project-card p {
    font-size: 12px;
  }
}
</style>
