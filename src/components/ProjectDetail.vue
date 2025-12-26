<template>
  <section class="project-detail" id="project-detail">
    <div class="container">
      <!-- Back Button -->
      <a href="#" @click.prevent="navigateTo('/projects-archive')" class="btn-back">← بازگشت به آرشیو</a>

      <!-- Loading State -->
      <Loader v-if="loading" />

      <!-- Error State -->
      <div v-if="error" class="error">
        <p>{{ error }}</p>
        <a href="#" @click.prevent="navigateTo('/projects-archive')" class="btn-back">بازگشت به آرشیو</a>
      </div>

      <!-- Project Content -->
      <article v-else-if="project" class="project-content">
        <!-- Project Title -->
        <h1 class="project-title">{{ project.title_fa || project.title_en }}</h1>
        
        <!-- Category Badge -->
        <div class="project-meta" v-if="project.category">
          <span class="category">{{ project.category }}</span>
        </div>

        <!-- Featured Image -->
        <div class="project-featured-image">
          <img :src="project.image_url || 'data:image/svg+xml/%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 1000 600%27%3E%3Crect fill=%27%23ddd%27 width=%271000%27 height=%27600%27/%3E%3C/svg%3E'" :alt="project.title_fa || project.title_en">
        </div>

        <!-- Iframe Section (if URL exists) - Displayed first for prominence -->
        <div v-if="project.iframe_url" class="iframe-section">
          <h2>پروژه تعاملی</h2>
          <div class="iframe-container">
            <iframe 
              :src="project.iframe_url" 
              title="Project Viewer"
              allow="fullscreen"
              allowfullscreen
            ></iframe>
          </div>
        </div>

        <!-- Project Description Section -->
        <div class="project-description">
          <h2>درباره‌ی پروژه</h2>
          <div class="description-content">
            <p>{{ project.description_fa || project.description_en }}</p>
          </div>

          <!-- Download Archive -->
          <div v-if="project.archive_url" class="download-section">
            <a :href="project.archive_url" download class="btn-download">
              دانلود آرشیو پروژه
            </a>
          </div>
        </div>

        <!-- Project Details Grid -->
        <div class="project-details-grid">
          <div class="detail-item">
            <h3>نوع پروژه</h3>
            <p>{{ project.category }}</p>
          </div>
          <div class="detail-item">
            <h3>تاریخ ایجاد</h3>
            <p>{{ formatDate(project.created_at) }}</p>
          </div>
          <div class="detail-item">
            <h3>آخرین بروزرسانی</h3>
            <p>{{ formatDate(project.updated_at) }}</p>
          </div>
        </div>

        <!-- Call to Action -->
        <div class="project-cta">
          <h3>آیا برای پروژه شما هم نیاز به خدمات مشابه دارید؟</h3>
          <a href="#" @click.prevent="goToContact" class="btn-contact">تماس با ما</a>
        </div>

        <!-- Related Projects -->
        <div class="related-projects" v-if="relatedProjects.length > 0">
          <h3>پروژه‌های مرتبط:</h3>
          <div class="related-grid">
            <a v-for="related in relatedProjects" :key="related.id" href="#" @click.prevent="navigateTo(`/project/${related.id}`)" class="related-card">
              <div class="related-image">
                <img :src="related.image_url || 'data:image/svg+xml/%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 200%27%3E%3Crect fill=%27%23ddd%27 width=%27300%27 height=%27200%27/%3E%3C/svg%3E'" :alt="related.title_fa || related.title_en">
              </div>
              <h4>{{ related.title_fa || related.title_en }}</h4>
            </a>
          </div>
        </div>
      </article>

      <!-- 404 Not Found -->
      <div v-else-if="!loading && !error" class="not-found">
        <p>پروژه مورد نظر یافت نشد.</p>
        <a href="#" @click.prevent="navigateTo('/projects-archive')" class="btn-back">بازگشت به آرشیو</a>
      </div>
    </div>
  </section>
</template>

<script>
import Loader from './Loader.vue';

export default {
  name: 'ProjectDetail',
  inject: ['navigateTo'],
  components: {
    Loader
  },
  data() {
    return {
      project: null,
      projects: [],
      relatedProjects: [],
      loading: false,
      error: null,
      projectId: null
    }
  },
  watch: {
    $route: {
      handler() {
        this.loadProject();
      },
      immediate: true
    }
  },
  mounted() {
    this.loadProject();
  },
  methods: {
    loadProject() {
      // Extract project ID from URL pathname
      const pathname = window.location.pathname;
      const match = pathname.match(/\/project\/(\d+)/);
      this.projectId = match ? parseInt(match[1]) : null;

      if (this.projectId) {
        this.fetchProject();
      }
    },
    async fetchProject() {
      this.loading = true;
      this.error = null;
      try {
        // Fetch from API
        const response = await fetch(`/api/projects/${this.projectId}`);
        
        if (!response.ok) {
          this.error = 'پروژه مورد نظر یافت نشد.';
          return;
        }

        this.project = await response.json();

        // Fetch all projects for related projects
        const allResponse = await fetch('/api/projects');
        const allProjects = await allResponse.json();

        // Get related projects (same category, different project)
        this.relatedProjects = allProjects
          .filter(p => p.category === this.project.category && p.id !== this.project.id)
          .slice(0, 3);

      } catch (err) {
        this.error = 'خطا در بارگذاری پروژه';
        console.error('Error fetching project:', err);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('fa-IR', options);
    },
    goToContact() {
      // Navigate to home page and scroll to contact section
      this.navigateTo('/');
      this.$nextTick(() => {
        setTimeout(() => {
          const contactElement = document.querySelector('#contact');
          if (contactElement) {
            contactElement.scrollIntoView({ behavior: 'smooth' });
          }
        }, 100);
      });
    }
  }
}
</script>

<style scoped>
.project-detail {
  padding: 60px 50px;
  background: #ffffff;
  min-height: 100vh;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.btn-back {
  display: inline-block;
  margin-bottom: 30px;
  color: #1abc9c;
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease-out;
}

.btn-back:hover {
  transform: translateX(4px);
}

/* Loading & Error States */
.loading, .error, .not-found {
  text-align: center;
  padding: 60px 20px;
  font-size: 16px;
}

.loading {
  color: #666;
}

.error, .not-found {
  background: #f5f5f5;
  border-radius: 2px;
}

.error {
  color: #d32f2f;
  background: #ffebee;
}

/* Project Title */
.project-title {
  font-size: 42px;
  font-weight: bold;
  line-height: 1.3;
  margin-bottom: 20px;
  color: #1a1a1a;
  text-align: right;
}

/* Category Badge */
.project-meta {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 30px;
}

.category {
  background: #1abc9c;
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 13px;
}

/* Featured Image */
.project-featured-image {
  width: 100%;
  height: 500px;
  margin-bottom: 50px;
  overflow: hidden;
  border-radius: 2px;
  background: #f5f5f5;
}

.project-featured-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Iframe Section */
.iframe-section {
  margin-bottom: 50px;
  text-align: right;
}

.iframe-section h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #1a1a1a;
}

.iframe-container {
  width: 100%;
  height: 900px;
  border: 1px solid #e8e8e8;
  border-radius: 2px;
  overflow: hidden;
  background: #f9f9f9;
}

.iframe-container iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* Description Section */
.project-description {
  margin-bottom: 50px;
  text-align: right;
}

.project-description h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #1a1a1a;
}

.description-content {
  font-size: 15px;
  line-height: 1.8;
  color: #333;
  margin-bottom: 25px;
}

.description-content p {
  margin-bottom: 15px;
}

/* Download Section */
.download-section {
  margin-top: 25px;
}

.btn-download {
  display: inline-block;
  padding: 12px 28px;
  background: #1abc9c;
  color: white;
  text-decoration: none;
  font-weight: 600;
  border-radius: 2px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-download:hover {
  background: #16a085;
  transform: scale(1.02);
}

/* Details Grid */
.project-details-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-bottom: 50px;
  padding: 30px;
  background: #f9f9f9;
  border: 1px solid #e8e8e8;
  text-align: right;
}

.detail-item h3 {
  font-size: 13px;
  font-weight: 600;
  color: #666;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-item p {
  font-size: 15px;
  color: #1a1a1a;
  font-weight: 500;
}

/* CTA Section */
.project-cta {
  text-align: center;
  padding: 50px 30px;
  background: #f9f9f9;
  border: 1px solid #e8e8e8;
  margin-bottom: 50px;
  border-radius: 2px;
}

.project-cta h3 {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #1a1a1a;
}

.btn-contact {
  display: inline-block;
  padding: 12px 40px;
  background: #1abc9c;
  color: white;
  text-decoration: none;
  font-weight: 600;
  border-radius: 2px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-contact:hover {
  background: #16a085;
  transform: scale(1.02);
}

/* Related Projects */
.related-projects {
  margin-top: 50px;
  text-align: right;
}

.related-projects h3 {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 25px;
  color: #1a1a1a;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.related-card {
  background: #ffffff;
  border: 1px solid #e8e8e8;
  border-radius: 2px;
  overflow: hidden;
  text-decoration: none;
  transition: all 0.3s ease-out;
}

.related-card:hover {
  border-color: #1abc9c;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.related-image {
  width: 100%;
  height: 150px;
  overflow: hidden;
  background: #f5f5f5;
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease-out;
}

.related-card:hover .related-image img {
  transform: scale(1.1);
}

.related-card h4 {
  font-size: 14px;
  font-weight: 600;
  padding: 15px;
  color: #1a1a1a;
  text-align: right;
  line-height: 1.4;
}

/* Responsive */
@media (max-width: 768px) {
  .project-detail {
    padding: 30px 20px;
  }

  .project-title {
    font-size: 28px;
  }

  .project-featured-image {
    height: 300px;
  }

  .iframe-container {
    height: 400px;
  }

  .project-description h2,
  .iframe-section h2 {
    font-size: 20px;
  }

  .project-details-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .project-cta {
    padding: 30px 20px;
  }

  .project-cta h3 {
    font-size: 18px;
  }

  .related-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}
</style>
