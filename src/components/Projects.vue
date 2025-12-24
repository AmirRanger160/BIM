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
        // Using sample data for now - replace with API call when frontend integration is set up
        this.projects = [
          {
            id: 1,
            title_en: 'BIM Modeling Project',
            title_fa: 'پروژه مدل‌سازی BIM',
            description_en: 'A comprehensive 3D BIM model created for a commercial building complex.',
            description_fa: 'یک مدل BIM سه‌بعدی جامع برای مجتمع تجاری ایجاد شده است.',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 250%27%3E%3Crect fill=%27%231abc9c%27 width=%27300%27 height=%27250%27/%3E%3Ctext x=%2750%25%27 y=%2750%25%27 text-anchor=%27middle%27 dy=%27.3em%27 fill=%27white%27 font-size=%2724%27%3EBIM Project 1%3C/text%3E%3C/svg%3E',
            iframe_url: null,
            archive_url: null,
            category: 'BIM'
          },
          {
            id: 2,
            title_en: '3D Point Cloud Processing',
            title_fa: 'پردازش ابر نقطه سه‌بعدی',
            description_en: 'Point cloud registration and processing for a historical structure survey.',
            description_fa: 'ثبت و پردازش ابر نقطه برای بررسی یک ساختار تاریخی.',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 250%27%3E%3Crect fill=%27%232d5f3f%27 width=%27300%27 height=%27250%27/%3E%3Ctext x=%2750%25%27 y=%2750%25%27 text-anchor=%27middle%27 dy=%27.3em%27 fill=%27white%27 font-size=%2724%27%3EPoint Cloud 2%3C/text%3E%3C/svg%3E',
            iframe_url: null,
            archive_url: null,
            category: 'Surveying'
          },
          {
            id: 3,
            title_en: 'Urban Survey Analysis',
            title_fa: 'تحلیل نقشه‌برداری شهری',
            description_en: 'Detailed surveying and documentation of urban development zone.',
            description_fa: 'نقشه‌برداری و مستندسازی دقیق منطقه توسعه شهری.',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 250%27%3E%3Crect fill=%27%23333%27 width=%27300%27 height=%27250%27/%3E%3Ctext x=%2750%25%27 y=%2750%25%27 text-anchor=%27middle%27 dy=%27.3em%27 fill=%27white%27 font-size=%2724%27%3EUrban Survey 3%3C/text%3E%3C/svg%3E',
            iframe_url: null,
            archive_url: null,
            category: 'Surveying'
          },
          {
            id: 4,
            title_en: 'Renovation Assessment',
            title_fa: 'ارزیابی نوسازی',
            description_en: 'Complete BIM assessment for building renovation project.',
            description_fa: 'ارزیابی جامع BIM برای پروژه نوسازی ساختمان.',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 250%27%3E%3Crect fill=%27%234a7c59%27 width=%27300%27 height=%27250%27/%3E%3Ctext x=%2750%25%27 y=%2750%25%27 text-anchor=%27middle%27 dy=%27.3em%27 fill=%27white%27 font-size=%2724%27%3ERenovation 4%3C/text%3E%3C/svg%3E',
            iframe_url: null,
            archive_url: null,
            category: 'BIM'
          },
          {
            id: 5,
            title_en: 'Infrastructure Mapping',
            title_fa: 'نقشه‌برداری زیرساخت',
            description_en: 'Large-scale infrastructure survey with laser scanning.',
            description_fa: 'نقشه‌برداری زیرساخت در مقیاس بزرگ با اسکن لیزری.',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 250%27%3E%3Crect fill=%27%235a8c6e%27 width=%27300%27 height=%27250%27/%3E%3Ctext x=%2750%25%27 y=%2750%25%27 text-anchor=%27middle%27 dy=%27.3em%27 fill=%27white%27 font-size=%2724%27%3EInfrastructure 5%3C/text%3E%3C/svg%3E',
            iframe_url: null,
            archive_url: null,
            category: 'Surveying'
          },
          {
            id: 6,
            title_en: 'Industrial Complex BIM',
            title_fa: 'BIM مجتمع صنعتی',
            description_en: 'BIM modeling of large industrial manufacturing facility.',
            description_fa: 'مدل‌سازی BIM تاسیسات تولید صنعتی بزرگ.',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 250%27%3E%3Crect fill=%27%236a5a3e%27 width=%27300%27 height=%27250%27/%3E%3Ctext x=%2750%25%27 y=%2750%25%27 text-anchor=%27middle%27 dy=%27.3em%27 fill=%27white%27 font-size=%2724%27%3EIndustrial 6%3C/text%3E%3C/svg%3E',
            iframe_url: null,
            archive_url: null,
            category: 'BIM'
          }
        ];
      } catch (err) {
        this.error = 'خطا در بارگذاری پروژه‌ها';
        console.error('Error fetching projects:', err);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.projects-section {
  padding: 60px 50px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-title {
  font-size: 32px;
  font-weight: bold;
  text-align: right;
  margin-bottom: 20px;
  color: #1a1a1a;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 50px;
  width: 100%;
  max-width: 1200px;
  margin-top: 50px;
}

.project-card {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  cursor: pointer;
  transition: all 0.3s ease-out;
  text-align: right;
  overflow: hidden;
}

.project-card:hover {
  border-color: #1abc9c;
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
  padding: 25px;
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
  background: #1abc9c;
  color: white;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  text-align: center;
  border: none;
  border-radius: 2px;
}

.btn-link:hover {
  background: #16a085;
  transform: scale(1.02);
}

.btn-link.secondary {
  background: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
}

.btn-link.secondary:hover {
  background: #e8e8e8;
  border-color: #1abc9c;
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
  background: #f0f0f0;
  color: #1abc9c;
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  border: 2px solid #1abc9c;
  border-radius: 2px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.btn-view-all:hover {
  background: #1abc9c;
  color: white;
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
