<template>
  <div class="project-page" :class="{ 'dark-mode': isDark }">
    <Navbar @toggle-theme="toggleTheme" :is-dark="isDark" />

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>در حال بارگیری پروژه...</p>
    </div>

    <!-- Error State -->
    <div v-if="error && !loading" class="error-container">
      <h2>خطا در بارگیری پروژه</h2>
      <p>{{ error }}</p>
      <router-link to="/media?tab=gallery" class="back-link">بازگشت به گالری</router-link>
    </div>

    <!-- Project Content -->
    <article v-if="project && !loading" 
             class="project-container"
             itemscope 
             itemtype="https://schema.org/CreativeWork">

      <!-- Breadcrumb -->
      <nav class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">
        <div class="container">
          <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <router-link to="/" itemprop="item">
              <span itemprop="name">خانه</span>
            </router-link>
            <meta itemprop="position" content="1" />
          </span>
          <span class="separator">/</span>
          <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <router-link to="/media?tab=gallery" itemprop="item">
              <span itemprop="name">گالری</span>
            </router-link>
            <meta itemprop="position" content="2" />
          </span>
          <span class="separator">/</span>
          <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <span class="current" itemprop="name">{{ project.title }}</span>
            <meta itemprop="position" content="3" />
          </span>
        </div>
      </nav>

      <!-- Project Header -->
      <header class="project-header">
        <div class="container">
          <div class="project-category" :style="{ background: project.categoryColor || '#667eea' }">
            {{ project.category }}
          </div>
          <h1 class="project-title" itemprop="name">{{ project.title }}</h1>
          <p class="project-description" itemprop="description">{{ project.description }}</p>
        </div>
      </header>

      <!-- Project Gallery -->
      <section class="project-gallery">
        <div class="container">
          <!-- Main Image -->
          <div class="main-image-container">
            <img 
              :src="currentImage" 
              :alt="project.title"
              class="main-image"
              @click="openLightbox(currentImageIndex)"
              itemprop="image"
            />
            <button 
              v-if="projectImages.length > 1"
              @click="previousImage" 
              class="gallery-nav prev"
              aria-label="تصویر قبل"
            >
              ‹
            </button>
            <button 
              v-if="projectImages.length > 1"
              @click="nextImage" 
              class="gallery-nav next"
              aria-label="تصویر بعد"
            >
              ›
            </button>
            <div class="image-counter" v-if="projectImages.length > 1">
              {{ currentImageIndex + 1 }} / {{ projectImages.length }}
            </div>
          </div>
          
          <!-- Thumbnails -->
          <div class="thumbnails" v-if="projectImages.length > 1">
            <div 
              v-for="(image, index) in projectImages" 
              :key="index"
              @click="currentImageIndex = index"
              :class="['thumbnail', { active: currentImageIndex === index }]"
            >
              <img :src="image" :alt="`${project.title} - تصویر ${index + 1}`" />
            </div>
          </div>
        </div>
      </section>
      
      <!-- Project Details -->
      <section class="project-details">
        <div class="container">
          <div class="details-grid">
            <!-- Main Content -->
            <div class="details-content">
              <h2>درباره پروژه</h2>
              <div class="project-text" itemprop="text">
                <div v-if="project.full_description" v-html="project.full_description"></div>
                <p v-else>{{ project.description }}</p>
              </div>
              
              <!-- Technologies Used -->
              <div class="technologies" v-if="project.tech && project.tech.length">
                <h3>تکنولوژی‌های استفاده شده</h3>
                <div class="tech-list">
                  <span 
                    v-for="tech in project.tech" 
                    :key="tech" 
                    class="tech-tag"
                    itemprop="keywords"
                  >
                    {{ tech }}
                  </span>
                </div>
              </div>
              
              <!-- Features -->
              <div class="features" v-if="project.features && project.features.length">
                <h3>ویژگی‌های پروژه</h3>
                <ul class="features-list">
                  <li v-for="feature in project.features" :key="feature">
                    <span class="feature-icon">✓</span>
                    {{ feature }}
                  </li>
                </ul>
              </div>
            </div>
            
            <!-- Sidebar -->
            <aside class="details-sidebar">
              <!-- Project Info Card -->
              <div class="info-card">
                <h3>اطلاعات پروژه</h3>
                <div class="info-list">
                  <div class="info-item">
                    <span class="info-label">وضعیت:</span>
                    <span class="info-value status" :class="project.status || 'completed'">
                      {{ getStatusText(project.status) }}
                    </span>
                  </div>
                  <div class="info-item" v-if="project.duration">
                    <span class="info-label">مدت زمان:</span>
                    <span class="info-value">{{ project.duration }}</span>
                  </div>
                  <div class="info-item" v-if="project.team">
                    <span class="info-label">تیم پروژه:</span>
                    <span class="info-value">{{ project.team }}</span>
                  </div>
                  <div class="info-item" v-if="project.budget">
                    <span class="info-label">بودجه:</span>
                    <span class="info-value">{{ project.budget }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Share -->
              <div class="share-card">
                <h3>اشتراک‌گذاری</h3>
                <div class="share-buttons">
                  <button @click="share('twitter')" class="share-btn" aria-label="اشتراک در توییتر">
                    🐦
                  </button>
                  <button @click="share('linkedin')" class="share-btn" aria-label="اشتراک در لینکدین">
                    💼
                  </button>
                  <button @click="share('telegram')" class="share-btn" aria-label="اشتراک در تلگرام">
                    ✈️
                  </button>
                  <button @click="share('whatsapp')" class="share-btn" aria-label="اشتراک در واتساپ">
                    💬
                  </button>
                </div>
              </div>
              
              <!-- CTA -->
              <div class="cta-card">
                <h3>پروژه مشابه می‌خواهید؟</h3>
                <p>با ما تماس بگیرید</p>
                <router-link to="/#contact" class="cta-btn">
                  تماس با ما
                </router-link>
              </div>
            </aside>
          </div>
        </div>
      </section>
      
      <!-- Related Projects -->
      <section class="related-projects" v-if="relatedProjects.length">
        <div class="container">
          <h2>پروژه‌های مرتبط</h2>
          <div class="related-grid">
            <router-link
              v-for="related in relatedProjects"
              :key="related.id"
              :to="`/project/${related.id}`"
              class="related-card"
            >
              <div class="related-image">
                <ImageSlider
                  :image="related.image"
                  :images="related.images"
                  :icon="related.icon"
                  :gradient="related.gradient"
                />
              </div>
              <div class="related-content">
                <h3>{{ related.title }}</h3>
                <p>{{ related.description }}</p>
                <span class="related-category">{{ related.category }}</span>
              </div>
            </router-link>
          </div>
        </div>
      </section>
      
      <!-- Navigation -->
      <div class="project-navigation">
        <div class="container">
          <router-link 
            v-if="previousProject" 
            :to="`/project/${previousProject.id}`"
            class="nav-btn prev-btn"
          >
            <span class="nav-arrow">←</span>
            <div class="nav-content">
              <span class="nav-label">پروژه قبلی</span>
              <span class="nav-title">{{ previousProject.title }}</span>
            </div>
          </router-link>
          <router-link 
            to="/media?tab=gallery"
            class="nav-btn all-btn"
          >
            <span>همه پروژه‌ها</span>
          </router-link>
          <router-link 
            v-if="nextProject" 
            :to="`/project/${nextProject.id}`"
            class="nav-btn next-btn"
          >
            <div class="nav-content">
              <span class="nav-label">پروژه بعدی</span>
              <span class="nav-title">{{ nextProject.title }}</span>
            </div>
            <span class="nav-arrow">→</span>
          </router-link>
        </div>
      </div>
      
      <!-- بخش نظرات -->
      <div class="container" v-if="project">
        <CommentSection
          content-type="project"
          :content-id="project.id"
          :is-dark="isDark"
        />
      </div>
    </article>
    
    <!-- Lightbox -->
    <Transition name="fade">
      <div v-if="lightboxOpen" class="lightbox" @click="closeLightbox">
        <button @click="closeLightbox" class="lightbox-close" aria-label="بستن">×</button>
        <button @click.stop="previousImageLightbox" class="lightbox-nav prev" aria-label="تصویر قبل">‹</button>
        <img :src="projectImages[lightboxIndex]" :alt="project.title" @click.stop />
        <button @click.stop="nextImageLightbox" class="lightbox-nav next" aria-label="تصویر بعد">›</button>
        <div class="lightbox-counter">{{ lightboxIndex + 1 }} / {{ projectImages.length }}</div>
      </div>
    </Transition>
    
    <Footer v-if="!loading" />
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getGalleryItem, getGalleryItems, getSlider } from '../api/services'
import ImageSlider from '../components/ImageSlider.vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import CommentSection from '../components/CommentSection.vue'

const route = useRoute()
const router = useRouter()
const { isDark, toggleTheme } = inject('theme')

const project = ref(null)
const relatedProjects = ref([])
const previousProject = ref(null)
const nextProject = ref(null)
const loading = ref(true)
const error = ref(null)

const formatDate = (dateString) => {
  if (!dateString) return 'نامشخص'
  try {
    return new Date(dateString).toLocaleDateString('fa-IR')
  } catch (e) {
    return dateString
  }
}

const enrichProjectWithSlider = async (projectData) => {
  if (projectData.slider_id) {
    try {
      const sliderResponse = await getSlider(projectData.slider_id)
      if (sliderResponse.data && sliderResponse.data.images) {
        return {
          ...projectData,
          images: sliderResponse.data.images
        }
      }
    } catch (err) {
      console.error('Error loading slider:', err)
    }
  }
  if (projectData.image && !projectData.images) {
    return {
      ...projectData,
      images: [projectData.image]
    }
  }
  return projectData
}

const fetchProject = async () => {
  try {
    loading.value = true
    error.value = null

    const projectId = route.params.id

    const response = await getGalleryItem(projectId)
    let projectData = response.data

    projectData = await enrichProjectWithSlider(projectData)
    project.value = projectData

    const allProjectsResponse = await getGalleryItems({ page: 1, limit: 100 })
    const allProjects = allProjectsResponse.data || []

    relatedProjects.value = await Promise.all(
      allProjects
        .filter(p => p.id !== projectData.id && p.category === projectData.category)
        .slice(0, 3)
        .map(p => enrichProjectWithSlider(p))
    )

    const currentIndex = allProjects.findIndex(p => p.id === projectData.id)
    if (currentIndex > 0) {
      nextProject.value = await enrichProjectWithSlider(allProjects[currentIndex - 1])
    }
    if (currentIndex < allProjects.length - 1) {
      previousProject.value = await enrichProjectWithSlider(allProjects[currentIndex + 1])
    }
  } catch (err) {
    console.error('Error fetching project:', err)
    error.value = 'خطا در بارگیری پروژه'
  } finally {
    loading.value = false
  }
}

watch(() => route.params.id, () => {
  if (route.params.id) {
    fetchProject()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
})

onMounted(() => {
  fetchProject()
})

const projectImages = computed(() => {
  if (!project.value) return []
  if (project.value.images && project.value.images.length) {
    return project.value.images
  }
  if (project.value.image) {
    return [project.value.image]
  }
  return []
})

const currentImageIndex = ref(0)

const currentImage = computed(() => {
  if (!projectImages.value.length) return ''
  return projectImages.value[currentImageIndex.value] || ''
})

const openLightbox = (index) => {
  currentImageIndex.value = index
  lightboxOpen.value = true
}

const closeLightbox = () => {
  lightboxOpen.value = false
}

const previousImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
  }
}

const nextImage = () => {
  if (currentImageIndex.value < projectImages.value.length - 1) {
    currentImageIndex.value++
  }
}

const lightboxOpen = ref(false)
const lightboxIndex = ref(0)

const previousImageLightbox = () => {
  if (lightboxIndex.value > 0) {
    lightboxIndex.value--
  }
}

const nextImageLightbox = () => {
  if (lightboxIndex.value < projectImages.value.length - 1) {
    lightboxIndex.value++
  }
}

const share = (platform) => {
  const url = window.location.href
  const text = project.value.title
  const encodedUrl = encodeURIComponent(url)
  const encodedText = encodeURIComponent(text)

  let shareUrl = ''
  if (platform === 'twitter') {
    shareUrl = `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedText}`
  } else if (platform === 'linkedin') {
    shareUrl = `https://www.linkedin.com/shareArticle?url=${encodedUrl}&title=${encodedText}`
  } else if (platform === 'telegram') {
    shareUrl = `https://t.me/share/url?url=${encodedUrl}&text=${encodedText}`
  } else if (platform === 'whatsapp') {
    shareUrl = `https://api.whatsapp.com/send?text=${encodedText} ${encodedUrl}`
  }

  window.open(shareUrl, '_blank')
}

const getStatusText = (status) => {
  const statusMap = {
    completed: 'تکمیل شده',
    ongoing: 'در حال انجام',
    pending: 'در انتظار',
  }
  return statusMap[status] || 'نامشخص'
}
</script>

<style scoped>
.project-page {
  min-height: 100vh;
  background: white;
  color: #1a1a1a;
}

.dark-mode.project-page {
  background: #1a1a1a;
  color: #ffffff;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Loading & Error */
.loading-container,
.error-container {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(102, 126, 234, 0.1);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.back-link {
  margin-top: 1rem;
  padding: 0.8rem 1.5rem;
  background: #667eea;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
}

.back-link:hover {
  background: #5568d3;
  transform: translateY(-2px);
}

/* Breadcrumb */
.breadcrumb {
  background: #f8f9fa;
  padding: 1rem 0;
  margin-top: 4rem;
}

.dark-mode .breadcrumb {
  background: #2d2d2d;
}

.breadcrumb .container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.breadcrumb a {
  color: #667eea;
  text-decoration: none;
}

.separator {
  color: #999;
}

.current {
  color: #666;
}

.dark-mode .current {
  color: #ccc;
}

/* Project Header */
.project-header {
  padding: 3rem 0;
  text-align: center;
}

.project-category {
  display: inline-block;
  padding: 0.5rem 1rem;
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.project-title {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1.3;
  margin-bottom: 1rem;
}

.project-description {
  font-size: 1.2rem;
  color: #666;
  line-height: 1.8;
  max-width: 800px;
  margin: 0 auto 2rem;
}

.dark-mode .project-description {
  color: #ccc;
}

.project-meta {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
  margin-top: 2rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
}

.dark-mode .meta-item {
  color: #ccc;
}

.meta-icon {
  font-size: 1.2rem;
}

.meta-label {
  font-weight: 600;
}

/* Project Body */
.project-body {
  padding: 2rem 0;
  background: #f9f9f9;
}

.dark-mode .project-body {
  background: #2c2c2c;
}

.project-text {
  font-size: 1.1rem;
  line-height: 1.9;
  color: #333;
  margin-bottom: 2rem;
}

.dark-mode .project-text {
  color: #ddd;
}

.project-text :deep(h2) {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 2rem 0 1rem;
  color: #1a1a1a;
}

.dark-mode .project-text :deep(h2) {
  color: white;
}

.project-text :deep(h3) {
  font-size: 1.4rem;
  font-weight: 600;
  margin: 1.5rem 0 0.8rem;
}

.project-text :deep(p) {
  margin-bottom: 1.5rem;
}

.project-text :deep(ul),
.project-text :deep(ol) {
  margin: 1.5rem 0;
  padding-right: 2rem;
}

.project-text :deep(li) {
  margin-bottom: 0.8rem;
}

.project-text :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  margin: 2rem 0;
}

.project-text :deep(blockquote) {
  border-right: 4px solid #667eea;
  padding: 1rem 1.5rem;
  margin: 2rem 0;
  background: #f8f9fa;
  border-radius: 8px;
  font-style: italic;
}

.dark-mode .project-text :deep(blockquote) {
  background: #2d2d2d;
}

.project-text :deep(span) {
  color: inherit;
}

.project-text :deep(br) {
  display: block;
  content: "";
}

.technologies,
.features {
  margin-top: 3rem;
}

.tech-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
}

.tech-tag {
  padding: 0.6rem 1.2rem;
  background: #f0f0f0;
  color: #667eea;
  border-radius: 20px;
  font-weight: 500;
}

.dark-mode .tech-tag {
  background: #3d3d3d;
}

.features-list {
  list-style: none;
  padding: 0;
}

.features-list li {
  padding: 0.8rem 0;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.dark-mode .features-list li {
  border-color: #444;
}

.feature-icon {
  color: #667eea;
  font-weight: bold;
  font-size: 1.2rem;
}

/* Project Gallery */
.project-gallery {
  padding: 3rem 0;
  background: #f8f9fa;
}

.dark-mode .project-gallery {
  background: #2d2d2d;
}

.main-image-container {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.main-image {
  width: 100%;
  height: 600px;
  object-fit: cover;
  cursor: zoom-in;
}

.gallery-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  font-size: 2rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gallery-nav:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
}

.gallery-nav.prev {
  right: 2rem;
}

.gallery-nav.next {
  left: 2rem;
}

.image-counter {
  position: absolute;
  bottom: 2rem;
  right: 2rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
}

.thumbnails {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.thumbnail {
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 3px solid transparent;
  transition: all 0.3s;
}

.thumbnail:hover,
.thumbnail.active {
  border-color: #667eea;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Sidebar */
.details-sidebar {
  position: sticky;
  top: 6rem;
}

.info-card,
.share-card,
.cta-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.dark-mode .info-card,
.dark-mode .share-card,
.dark-mode .cta-card {
  background: #2d2d2d;
}

.info-card h3,
.share-card h3,
.cta-card h3 {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  font-weight: 600;
  color: #666;
}

.dark-mode .info-label {
  color: #ccc;
}

.status {
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status.completed {
  background: #d4edda;
  color: #155724;
}

.share-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.8rem;
}

.share-btn {
  padding: 0.8rem;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
}

.dark-mode .share-btn {
  background: #3d3d3d;
}

.share-btn:hover {
  transform: translateY(-3px);
}

.cta-card {
  text-align: center;
}

.cta-card p {
  margin: 0.5rem 0 1rem;
  color: #666;
}

.dark-mode .cta-card p {
  color: #ccc;
}

.cta-btn {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  background: #667eea;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}

.cta-btn:hover {
  background: #5568d3;
  transform: translateY(-2px);
}

/* Related Projects */
.related-projects {
  padding: 4rem 0;
  background: #f8f9fa;
}

.dark-mode .related-projects {
  background: #2d2d2d;
}

.related-projects h2 {
  text-align: center;
  margin-bottom: 3rem;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.related-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.dark-mode .related-card {
  background: #1a1a1a;
}

.related-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.related-image {
  height: 200px;
}

.related-content {
  padding: 1.5rem;
}

.related-content h3 {
  margin-bottom: 0.5rem;
}

.related-content p {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.dark-mode .related-content p {
  color: #ccc;
}

.related-category {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  background: #667eea;
  color: white;
  border-radius: 12px;
  font-size: 0.8rem;
}

/* Navigation */
.project-navigation {
  padding: 3rem 0;
  border-top: 1px solid #e0e0e0;
}

.dark-mode .project-navigation {
  border-color: #444;
}

.project-navigation .container {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1rem;
  align-items: center;
}

.nav-btn {
  padding: 1.5rem;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.dark-mode .nav-btn {
  background: #2d2d2d;
  border-color: #444;
}

.nav-btn:hover {
  border-color: #667eea;
  transform: translateY(-3px);
}

.nav-content {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.nav-label {
  font-size: 0.85rem;
  color: #999;
}

.nav-title {
  font-weight: 600;
  color: #667eea;
}

.nav-arrow {
  font-size: 2rem;
  color: #667eea;
}

.all-btn {
  justify-content: center;
  background: #667eea;
  color: white;
  border-color: #667eea;
}

/* Lightbox */
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.lightbox img {
  max-width: 90%;
  max-height: 90vh;
  border-radius: 8px;
}

.lightbox-close {
  position: absolute;
  top: 2rem;
  left: 2rem;
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  font-size: 2rem;
  cursor: pointer;
  transition: all 0.3s;
}

.lightbox-close:hover {
  background: white;
  transform: scale(1.1);
}

.lightbox-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  font-size: 2rem;
  cursor: pointer;
  transition: all 0.3s;
}

.lightbox-nav:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
}

.lightbox-nav.prev {
  right: 4rem;
}

.lightbox-nav.next {
  left: 4rem;
}

.lightbox-counter {
  position: absolute;
  bottom: 2rem;
  right: 50%;
  transform: translateX(50%);
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  font-weight: 600;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 1024px) {
  .details-grid,
  .project-navigation .container {
    grid-template-columns: 1fr;
  }
  
  .details-sidebar {
    position: static;
  }
}

@media (max-width: 768px) {
  .project-title {
    font-size: 1.8rem;
  }
  
  .main-image {
    height: 300px;
  }
  
  .gallery-nav {
    width: 40px;
    height: 40px;
  }
  
  .gallery-nav.prev {
    right: 1rem;
  }
  
  .gallery-nav.next {
    left: 1rem;
  }
  
  .related-grid {
    grid-template-columns: 1fr;
  }
}
</style>
