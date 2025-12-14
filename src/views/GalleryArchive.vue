<template>
  <div class="archive-page" :class="{ 'dark-mode': isDark }">
    <Navbar @toggle-theme="toggleTheme" :is-dark="isDark" />
    
    <section class="archive-hero">
      <div class="container">
        <div class="breadcrumb">
          <router-link to="/">خانه</router-link>
          <span class="separator">/</span>
          <span class="current">گالری</span>
        </div>
        <h1 class="page-title">آرشیو کامل گالری</h1>
        <p class="page-description">تمام پروژه‌ها و نمونه کارهای ما در یک نگاه</p>
      </div>
    </section>

    <section class="archive-content">
      <div class="container">
        <!-- Search and Filter -->
        <div class="archive-controls">
          <div class="search-box">
            <span class="search-icon">🔍</span>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="جستجو در پروژه‌ها..."
              class="search-input"
            />
          </div>
          
          <div class="filter-buttons">
            <button 
              v-for="category in categories" 
              :key="category"
              @click="selectedCategory = category"
              :class="['filter-btn', { active: selectedCategory === category }]"
            >
              {{ category }}
            </button>
          </div>

          <div class="view-toggle">
            <button @click="viewMode = 'grid'" :class="{ active: viewMode === 'grid' }">
              <span>⊞</span>
            </button>
            <button @click="viewMode = 'list'" :class="{ active: viewMode === 'list' }">
              <span>☰</span>
            </button>
          </div>
        </div>

        <div class="results-info">
          <span class="results-count">{{ filteredItems.length }} پروژه یافت شد</span>
        </div>

        <!-- Gallery Grid/List -->
        <TransitionGroup 
          name="gallery-list" 
          tag="div" 
          :class="['gallery-archive-grid', viewMode]"
        >
          <div 
            v-for="item in paginatedItems" 
            :key="item.id" 
            class="gallery-card"
            @click="openModal(item)"
          >
            <div class="card-image" :style="{ background: item.gradient }">
              <div class="card-overlay">
                <div class="card-icon">{{ item.icon }}</div>
                <div class="overlay-content">
                  <span class="view-btn">مشاهده پروژه</span>
                </div>
              </div>
              <div class="card-badge" :style="{ background: item.categoryColor }">
                {{ item.category }}
              </div>
              <div class="card-stats">
                <span>👁️ {{ item.views }}</span>
                <span>💬 {{ item.comments }}</span>
              </div>
            </div>
            
            <div class="card-content">
              <h3 class="card-title">{{ item.title }}</h3>
              <p class="card-description">{{ item.description }}</p>
              <div class="card-meta">
                <span class="card-date">{{ item.date }}</span>
                <div class="card-tech">
                  <span v-for="tech in item.technologies.slice(0, 3)" :key="tech" class="tech-tag">
                    {{ tech }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </TransitionGroup>

        <!-- Pagination -->
        <div v-if="filteredItems.length > itemsPerPage" class="pagination">
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1"
            class="pagination-btn"
          >
            قبلی
          </button>
          
          <div class="pagination-pages">
            <button
              v-for="page in totalPages"
              :key="page"
              @click="currentPage = page"
              :class="['page-btn', { active: currentPage === page }]"
            >
              {{ page }}
            </button>
          </div>
          
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            class="pagination-btn"
          >
            بعدی
          </button>
        </div>
      </div>
    </section>

    <!-- Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedItem" class="modal-overlay" @click="closeModal">
          <div class="modal-content" @click.stop>
            <button class="modal-close" @click="closeModal">✕</button>
            
            <div class="modal-image" :style="{ background: selectedItem.gradient }">
              <span class="modal-icon">{{ selectedItem.icon }}</span>
            </div>
            
            <div class="modal-body">
              <div class="modal-header">
                <h2 class="modal-title">{{ selectedItem.title }}</h2>
                <div class="modal-category" :style="{ background: selectedItem.categoryColor }">
                  {{ selectedItem.category }}
                </div>
              </div>
              
              <p class="modal-description">{{ selectedItem.description }}</p>
              
              <div class="modal-details">
                <div class="detail-item">
                  <span class="detail-label">مدت زمان:</span>
                  <span class="detail-value">{{ selectedItem.duration }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">تاریخ:</span>
                  <span class="detail-value">{{ selectedItem.date }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">بازدید:</span>
                  <span class="detail-value">{{ selectedItem.views }}</span>
                </div>
              </div>
              
              <div class="modal-tech">
                <h4>تکنولوژی‌های استفاده شده:</h4>
                <div class="tech-tags">
                  <span v-for="tech in selectedItem.technologies" :key="tech" class="tech-tag">
                    {{ tech }}
                  </span>
                </div>
              </div>

              <div class="modal-actions">
                <button class="action-btn primary">مشاهده دمو</button>
                <button class="action-btn secondary">دانلود کیس استادی</button>
              </div>
            </div>

            <button class="modal-nav prev" @click.stop="previousItem">←</button>
            <button class="modal-nav next" @click.stop="nextItem">→</button>
          </div>
        </div>
      </Transition>
    </Teleport>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

// Inject theme from App.vue
const { isDark, toggleTheme } = inject('theme')

const searchQuery = ref('')
const selectedCategory = ref('همه')
const viewMode = ref('grid')
const currentPage = ref(1)
const itemsPerPage = 12
const selectedItem = ref(null)

const categories = ['همه', 'وب اپلیکیشن', 'موبایل اپ', 'طراحی رابط', 'برندینگ', 'داشبورد']

const galleryItems = ref([
  {
    id: 1,
    title: 'داشبورد مدیریتی پیشرفته',
    description: 'سیستم جامع مدیریت با امکانات گسترده برای کنترل کامل کسب و کار',
    icon: '📊',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    category: 'داشبورد',
    categoryColor: '#667eea',
    date: 'دی ۱۴۰۳',
    duration: '۳ ماه',
    views: '۵٫۲ هزار',
    comments: '۱۲۳',
    technologies: ['Vue.js', 'Node.js', 'MongoDB', 'Chart.js', 'Socket.io']
  },
  {
    id: 2,
    title: 'اپلیکیشن موبایل فروشگاهی',
    description: 'اپلیکیشن فروشگاه آنلاین با تجربه کاربری عالی و امکانات پیشرفته',
    icon: '📱',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    category: 'موبایل اپ',
    categoryColor: '#f093fb',
    date: 'آذر ۱۴۰۳',
    duration: '۴ ماه',
    views: '۷٫۸ هزار',
    comments: '۲۴۵',
    technologies: ['React Native', 'Redux', 'Firebase', 'Stripe']
  },
  {
    id: 3,
    title: 'وب‌سایت شرکتی مدرن',
    description: 'طراحی و توسعه وبسایت شرکتی با استانداردهای روز دنیا',
    icon: '🌐',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    category: 'وب اپلیکیشن',
    categoryColor: '#4facfe',
    date: 'آبان ۱۴۰۳',
    duration: '۲ ماه',
    views: '۳٫۵ هزار',
    comments: '۸۹',
    technologies: ['Next.js', 'TypeScript', 'Tailwind CSS', 'Vercel']
  },
  {
    id: 4,
    title: 'سیستم رزرو آنلاین',
    description: 'پلتفرم رزرواسیون هوشمند برای هتل‌ها و رستوران‌ها',
    icon: '🎫',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    category: 'وب اپلیکیشن',
    categoryColor: '#43e97b',
    date: 'مهر ۱۴۰۳',
    duration: '۵ ماه',
    views: '۴٫۳ هزار',
    comments: '۱۵۶',
    technologies: ['Laravel', 'Vue.js', 'MySQL', 'Redis']
  },
  {
    id: 5,
    title: 'طراحی هویت بصری برند',
    description: 'ایجاد هویت بصری کامل شامل لوگو، رنگ و تایپوگرافی',
    icon: '🎨',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    category: 'برندینگ',
    categoryColor: '#fa709a',
    date: 'شهریور ۱۴۰۳',
    duration: '۱ ماه',
    views: '۲٫۹ هزار',
    comments: '۶۷',
    technologies: ['Figma', 'Adobe Illustrator', 'Adobe Photoshop']
  },
  {
    id: 6,
    title: 'رابط کاربری اپلیکیشن بانکی',
    description: 'طراحی UI/UX مدرن برای اپلیکیشن بانکداری موبایل',
    icon: '💳',
    gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    category: 'طراحی رابط',
    categoryColor: '#30cfd0',
    date: 'مرداد ۱۴۰۳',
    duration: '۳ ماه',
    views: '۶٫۱ هزار',
    comments: '۱۹۸',
    technologies: ['Figma', 'Sketch', 'Principle', 'InVision']
  },
  {
    id: 7,
    title: 'پلتفرم یادگیری آنلاین',
    description: 'سیستم مدیریت آموزش (LMS) با قابلیت‌های پیشرفته',
    icon: '🎓',
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    category: 'وب اپلیکیشن',
    categoryColor: '#a8edea',
    date: 'تیر ۱۴۰۳',
    duration: '۶ ماه',
    views: '۸٫۵ هزار',
    comments: '۳۱۲',
    technologies: ['Django', 'React', 'PostgreSQL', 'WebRTC']
  },
  {
    id: 8,
    title: 'اپلیکیشن تناسب اندام',
    description: 'برنامه ورزشی هوشمند با برنامه‌ریزی شخصی‌سازی شده',
    icon: '💪',
    gradient: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
    category: 'موبایل اپ',
    categoryColor: '#ff9a9e',
    date: 'خرداد ۱۴۰۳',
    duration: '۴ ماه',
    views: '۵٫۷ هزار',
    comments: '۱۸۹',
    technologies: ['Flutter', 'Firebase', 'TensorFlow Lite']
  }
])

const filteredItems = computed(() => {
  let filtered = galleryItems.value

  if (selectedCategory.value !== 'همه') {
    filtered = filtered.filter(item => item.category === selectedCategory.value)
  }

  if (searchQuery.value) {
    filtered = filtered.filter(item =>
      item.title.includes(searchQuery.value) ||
      item.description.includes(searchQuery.value) ||
      item.technologies.some(tech => tech.includes(searchQuery.value))
    )
  }

  return filtered
})

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredItems.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredItems.value.length / itemsPerPage)
})

const openModal = (item) => {
  selectedItem.value = item
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  selectedItem.value = null
  document.body.style.overflow = ''
}

const nextItem = () => {
  const currentIndex = galleryItems.value.findIndex(item => item.id === selectedItem.value.id)
  const nextIndex = (currentIndex + 1) % galleryItems.value.length
  selectedItem.value = galleryItems.value[nextIndex]
}

const previousItem = () => {
  const currentIndex = galleryItems.value.findIndex(item => item.id === selectedItem.value.id)
  const prevIndex = (currentIndex - 1 + galleryItems.value.length) % galleryItems.value.length
  selectedItem.value = galleryItems.value[prevIndex]
}
</script>

<style scoped>
.archive-page {
  min-height: 100vh;
  background: white;
  color: #1a1a1a;
}

.dark-mode.archive-page {
  background: #1a1a1a;
  color: #ffffff;
}

.archive-hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 8rem 0 4rem;
  text-align: center;
  color: white;
}

.dark-mode .archive-hero {
  background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.breadcrumb {
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

.breadcrumb a {
  color: white;
  text-decoration: none;
  transition: opacity 0.3s;
}

.breadcrumb a:hover {
  opacity: 0.7;
}

.separator {
  margin: 0 0.5rem;
}

.current {
  opacity: 0.7;
}

.page-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
}

.page-description {
  font-size: 1.2rem;
  opacity: 0.9;
}

.archive-content {
  padding: 4rem 0;
  background: white;
}

.dark-mode .archive-content {
  background: #1a1a1a;
}

.archive-controls {
  display: flex;
  gap: 2rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  flex: 1;
  min-width: 250px;
  position: relative;
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
}

.search-input {
  width: 100%;
  padding: 1rem 3rem 1rem 1rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  font-size: 1rem;
  transition: all 0.3s;
  background: white;
}

.dark-mode .search-input {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  color: #1a1a1a;
}

.dark-mode .filter-btn {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.filter-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.view-toggle {
  display: flex;
  gap: 0.5rem;
}

.view-toggle button {
  width: 45px;
  height: 45px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background: white;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s;
}

.dark-mode .view-toggle button {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.view-toggle button.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.results-info {
  margin-bottom: 2rem;
}

.results-count {
  font-weight: 600;
  color: #6c757d;
}

.dark-mode .results-count {
  color: #a0a0a0;
}

.gallery-archive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.gallery-archive-grid.list {
  grid-template-columns: 1fr;
}

.gallery-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s;
  border: 1px solid rgba(0, 0, 0, 0.05);
  cursor: pointer;
}

.dark-mode .gallery-card {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

.gallery-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.card-image {
  height: 220px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.gallery-card:hover .card-overlay {
  background: rgba(0, 0, 0, 0.7);
}

.card-icon {
  font-size: 4rem;
  transition: all 0.3s;
}

.gallery-card:hover .card-icon {
  transform: scale(1.2);
}

.overlay-content {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.3s;
}

.gallery-card:hover .overlay-content {
  opacity: 1;
  transform: translateY(0);
}

.view-btn {
  background: white;
  color: #667eea;
  padding: 0.75rem 2rem;
  border-radius: 50px;
  font-weight: 600;
  display: inline-block;
}

.card-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  color: white;
  font-size: 0.85rem;
  font-weight: 600;
}

.card-stats {
  position: absolute;
  bottom: 1rem;
  left: 1rem;
  display: flex;
  gap: 1rem;
  color: white;
  font-size: 0.9rem;
}

.card-content {
  padding: 2rem;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #1a1a1a;
}

.dark-mode .card-title {
  color: #ffffff;
}

.card-description {
  color: #6c757d;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.dark-mode .card-description {
  color: #a0a0a0;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.card-date {
  color: #6c757d;
  font-size: 0.9rem;
}

.dark-mode .card-date {
  color: #a0a0a0;
}

.card-tech {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tech-tag {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 3rem;
}

.pagination-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 10px;
  background: white;
  color: #667eea;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.dark-mode .pagination-btn {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(102, 126, 234, 0.3);
}

.pagination-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.pagination-pages {
  display: flex;
  gap: 0.5rem;
}

.page-btn {
  width: 45px;
  height: 45px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background: white;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.dark-mode .page-btn {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.page-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 2rem;
  overflow-y: auto;
}

.modal-content {
  background: white;
  border-radius: 25px;
  max-width: 900px;
  width: 100%;
  position: relative;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.dark-mode .modal-content {
  background: #2d2d2d;
}

.modal-close {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: #1a1a1a;
  z-index: 10;
}

.dark-mode .modal-close {
  background: rgba(0, 0, 0, 0.5);
  color: #ffffff;
}

.modal-close:hover {
  background: rgba(255, 0, 0, 0.1);
  color: #ff0000;
  transform: scale(1.1);
}

.modal-image {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-icon {
  font-size: 6rem;
}

.modal-body {
  padding: 3rem;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 2rem;
  gap: 2rem;
}

.modal-title {
  font-size: 2rem;
  font-weight: 800;
  color: #1a1a1a;
  flex: 1;
}

.dark-mode .modal-title {
  color: #ffffff;
}

.modal-category {
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  color: white;
  font-weight: 600;
  white-space: nowrap;
}

.modal-description {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #6c757d;
  margin-bottom: 2rem;
}

.dark-mode .modal-description {
  color: #a0a0a0;
}

.modal-details {
  background: rgba(102, 126, 234, 0.05);
  padding: 2rem;
  border-radius: 15px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.dark-mode .modal-details {
  background: rgba(102, 126, 234, 0.1);
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-label {
  font-weight: 600;
  color: #6c757d;
  font-size: 0.9rem;
}

.dark-mode .detail-label {
  color: #a0a0a0;
}

.detail-value {
  font-weight: 700;
  color: #667eea;
  font-size: 1.1rem;
}

.modal-tech {
  margin-bottom: 2rem;
}

.modal-tech h4 {
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.dark-mode .modal-tech h4 {
  color: #ffffff;
}

.tech-tags {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  font-size: 1rem;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.action-btn.secondary {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.action-btn.secondary:hover {
  background: rgba(102, 126, 234, 0.2);
}

.modal-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1a1a1a;
}

.modal-nav.prev {
  right: 1.5rem;
}

.modal-nav.next {
  left: 1.5rem;
}

.modal-nav:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-50%) scale(1.1);
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9);
}

.gallery-list-enter-active,
.gallery-list-leave-active {
  transition: all 0.5s ease;
}

.gallery-list-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.gallery-list-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.gallery-list-move {
  transition: transform 0.5s ease;
}

@media (max-width: 1024px) {
  .archive-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2.5rem;
  }
  
  .gallery-archive-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-body {
    padding: 2rem;
  }
  
  .modal-header {
    flex-direction: column;
  }
  
  .modal-title {
    font-size: 1.5rem;
  }
  
  .pagination-pages {
    flex-wrap: wrap;
  }
}
</style>
