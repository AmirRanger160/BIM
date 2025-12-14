<template>
  <div class="archive-page" :class="{ 'dark-mode': isDark }">
    <Navbar @toggle-theme="toggleTheme" :is-dark="isDark" />
    
    <section class="archive-hero">
      <div class="container">
        <div class="breadcrumb">
          <router-link to="/">خانه</router-link>
          <span class="separator">/</span>
          <span class="current">مقالات</span>
        </div>
        <h1 class="page-title">آرشیو کامل مقالات</h1>
        <p class="page-description">تمام مقالات، آموزش‌ها و اخبار تکنولوژی در یک مکان</p>
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
              placeholder="جستجو در مقالات..."
              class="search-input"
            />
          </div>
          
          <div class="filter-tabs">
            <button 
              v-for="category in categories" 
              :key="category"
              @click="selectedCategory = category"
              :class="['filter-btn', { active: selectedCategory === category }]"
            >
              <span class="filter-text">{{ category }}</span>
              <span v-if="selectedCategory === category" class="active-indicator"></span>
            </button>
          </div>

          <select v-model="sortBy" class="sort-select">
            <option value="latest">جدیدترین</option>
            <option value="popular">محبوب‌ترین</option>
            <option value="trending">پربازدیدترین</option>
          </select>
        </div>

        <div class="results-info">
          <span class="results-count">{{ filteredArticles.length }} مقاله یافت شد</span>
        </div>

        <!-- Articles Grid -->
        <TransitionGroup name="article-list" tag="div" class="articles-archive-grid">
          <article 
            v-for="article in paginatedArticles" 
            :key="article.id" 
            class="article-card"
            @click="openArticle(article)"
          >
            <div class="article-image" :style="{ background: article.gradient }">
              <span class="article-icon">{{ article.icon }}</span>
              <div class="article-category">{{ article.category }}</div>
              <div v-if="article.featured" class="featured-badge">ویژه</div>
            </div>
            
            <div class="article-content">
              <div class="article-meta">
                <span class="article-date">{{ article.date }}</span>
                <span class="article-read-time">{{ article.readTime }}</span>
                <span class="article-views">👁️ {{ article.views }}</span>
              </div>
              
              <h3 class="article-title">{{ article.title }}</h3>
              <p class="article-excerpt">{{ article.excerpt }}</p>
              
              <div class="article-tags-preview">
                <span v-for="tag in article.tags.slice(0, 3)" :key="tag" class="tag-mini">
                  {{ tag }}
                </span>
              </div>
              
              <div class="article-footer">
                <div class="article-author">
                  <div class="author-avatar">{{ article.authorAvatar }}</div>
                  <span class="author-name">{{ article.author }}</span>
                </div>
                <span class="read-more">
                  بیشتر
                  <span class="arrow">←</span>
                </span>
              </div>
            </div>
          </article>
        </TransitionGroup>

        <!-- Pagination -->
        <div v-if="filteredArticles.length > articlesPerPage" class="pagination">
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

    <!-- Article Detail Modal -->
    <Transition name="slide-fade">
      <ArticleDetail 
        v-if="selectedArticle" 
        :article="selectedArticle" 
        @close="closeArticle"
      />
    </Transition>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import ArticleDetail from '../components/ArticleDetail.vue'

// Inject theme from App.vue
const { isDark, toggleTheme } = inject('theme')

const searchQuery = ref('')
const selectedCategory = ref('همه')
const sortBy = ref('latest')
const currentPage = ref(1)
const articlesPerPage = 12
const selectedArticle = ref(null)

const categories = ['همه', 'طراحی', 'برنامه‌نویسی', 'هوش مصنوعی', 'امنیت', 'موبایل']

const articles = ref([
  {
    id: 1,
    title: 'آینده طراحی وب در سال ۲۰۲۵',
    excerpt: 'بررسی جامع ترندهای جدید طراحی وب و تجربه کاربری که در سال آینده صنعت را متحول خواهند کرد.',
    date: '۱۴ دی ۱۴۰۴',
    readTime: '۵ دقیقه',
    category: 'طراحی',
    icon: '📰',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    author: 'محمد احمدی',
    authorAvatar: 'م',
    authorRole: 'طراح ارشد UI/UX',
    views: '۲٫۵ هزار',
    viewsNum: 2500,
    featured: true,
    tags: ['طراحی وب', 'UI/UX', 'ترند ۲۰۲۵', 'تجربه کاربری'],
    fullContent: `<h2>مقدمه</h2><p>دنیای طراحی وب همواره در حال تحول است...</p>`
  },
  {
    id: 2,
    title: 'آموزش کامل Vue.js 3 برای مبتدیان',
    excerpt: 'راهنمای جامع یادگیری Vue.js 3 از صفر تا صد با مثال‌های کاربردی و پروژه‌های واقعی.',
    date: '۱۲ دی ۱۴۰۴',
    readTime: '۱۵ دقیقه',
    category: 'برنامه‌نویسی',
    icon: '💻',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    author: 'سارا محمدی',
    authorAvatar: 'س',
    authorRole: 'توسعه‌دهنده Frontend',
    views: '۳٫۸ هزار',
    viewsNum: 3800,
    featured: true,
    tags: ['Vue.js', 'JavaScript', 'آموزش', 'Frontend'],
    fullContent: `<h2>مقدمه به Vue.js</h2><p>Vue.js یکی از محبوب‌ترین فریمورک‌های JavaScript است...</p>`
  },
  {
    id: 3,
    title: 'بهترین شیوه‌های امنیتی در برنامه‌نویسی',
    excerpt: 'نکات کلیدی و بهترین روش‌ها برای ایمن‌سازی کدهای خود و محافظت از داده‌های کاربران.',
    date: '۱۰ دی ۱۴۰۴',
    readTime: '۸ دقیقه',
    category: 'امنیت',
    icon: '🔒',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    author: 'علی رضایی',
    authorAvatar: 'ع',
    authorRole: 'متخصص امنیت',
    views: '۱٫۹ هزار',
    viewsNum: 1900,
    featured: false,
    tags: ['امنیت', 'Security', 'Best Practices', 'Cybersecurity'],
    fullContent: `<h2>اهمیت امنیت در برنامه‌نویسی</h2><p>امنیت یکی از مهم‌ترین جنبه‌های توسعه نرم‌افزار است...</p>`
  },
  {
    id: 4,
    title: 'معرفی هوش مصنوعی ChatGPT و کاربردها',
    excerpt: 'آشنایی با قابلیت‌های ChatGPT و نحوه استفاده از آن در پروژه‌های واقعی.',
    date: '۸ دی ۱۴۰۴',
    readTime: '۱۰ دقیقه',
    category: 'هوش مصنوعی',
    icon: '🤖',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    author: 'فاطمه کریمی',
    authorAvatar: 'ف',
    authorRole: 'پژوهشگر AI',
    views: '۵٫۲ هزار',
    viewsNum: 5200,
    featured: true,
    tags: ['هوش مصنوعی', 'ChatGPT', 'AI', 'Machine Learning'],
    fullContent: `<h2>ChatGPT چیست؟</h2><p>ChatGPT یک مدل زبانی قدرتمند است که توسط OpenAI توسعه یافته...</p>`
  },
  {
    id: 5,
    title: 'طراحی اپلیکیشن موبایل: نکات کلیدی',
    excerpt: 'راهنمای عملی طراحی رابط کاربری برای اپلیکیشن‌های موبایل با تمرکز بر تجربه کاربری.',
    date: '۶ دی ۱۴۰۴',
    readTime: '۷ دقیقه',
    category: 'موبایل',
    icon: '📱',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    author: 'رضا حسینی',
    authorAvatar: 'ر',
    authorRole: 'طراح موبایل',
    views: '۲٫۳ هزار',
    viewsNum: 2300,
    featured: false,
    tags: ['موبایل', 'UI/UX', 'اپلیکیشن', 'طراحی'],
    fullContent: `<h2>اصول طراحی موبایل</h2><p>طراحی رابط کاربری موبایل نیازمند دقت و توجه ویژه است...</p>`
  },
  {
    id: 6,
    title: 'React vs Vue: کدام را انتخاب کنیم؟',
    excerpt: 'مقایسه جامع دو فریمورک محبوب React و Vue برای انتخاب بهتر در پروژه بعدی شما.',
    date: '۴ دی ۱۴۰۴',
    readTime: '۱۲ دقیقه',
    category: 'برنامه‌نویسی',
    icon: '⚛️',
    gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    author: 'مهدی جعفری',
    authorAvatar: 'م',
    authorRole: 'توسعه‌دهنده Full Stack',
    views: '۴٫۱ هزار',
    viewsNum: 4100,
    featured: false,
    tags: ['React', 'Vue', 'JavaScript', 'Frontend'],
    fullContent: `<h2>مقدمه</h2><p>انتخاب بین React و Vue یکی از سوالات رایج توسعه‌دهندگان است...</p>`
  }
])

const filteredArticles = computed(() => {
  let filtered = articles.value

  if (selectedCategory.value !== 'همه') {
    filtered = filtered.filter(article => article.category === selectedCategory.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(article =>
      article.title.toLowerCase().includes(query) ||
      article.excerpt.toLowerCase().includes(query) ||
      article.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }

  if (sortBy.value === 'popular') {
    filtered = [...filtered].sort((a, b) => b.viewsNum - a.viewsNum)
  } else if (sortBy.value === 'latest') {
    filtered = [...filtered].sort((a, b) => b.id - a.id)
  }

  return filtered
})

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * articlesPerPage
  const end = start + articlesPerPage
  return filteredArticles.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredArticles.value.length / articlesPerPage)
})

const openArticle = (article) => {
  selectedArticle.value = article
}

const closeArticle = () => {
  selectedArticle.value = null
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

.filter-tabs {
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
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-weight: 600;
  color: #1a1a1a;
  position: relative;
  overflow: hidden;
}

.filter-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  z-index: 0;
}

.filter-btn:hover::before {
  width: 300px;
  height: 300px;
}

.filter-text {
  position: relative;
  z-index: 1;
  transition: color 0.3s;
}

.filter-btn:hover .filter-text {
  color: white;
}

.active-indicator {
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 3px;
  background: white;
  border-radius: 3px 3px 0 0;
  animation: indicator-slide 0.4s ease;
}

@keyframes indicator-slide {
  from {
    width: 0%;
    opacity: 0;
  }
  to {
    width: 80%;
    opacity: 1;
  }
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
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.filter-btn.active .filter-text {
  color: white;
}

.sort-select {
  padding: 0.75rem 1.5rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  background: white;
  cursor: pointer;
  font-weight: 600;
  color: #1a1a1a;
}

.dark-mode .sort-select {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
  color: white;
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

.articles-archive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

/* TransitionGroup Animations */
.article-list-move,
.article-list-enter-active,
.article-list-leave-active {
  transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.article-list-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}

.article-list-leave-to {
  opacity: 0;
  transform: translateY(-30px) scale(0.9);
}

.article-list-leave-active {
  position: absolute;
}

.article-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s;
  border: 1px solid rgba(0, 0, 0, 0.05);
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.dark-mode .article-card {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

.article-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.article-image {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.article-icon {
  font-size: 4rem;
  transition: transform 0.3s;
}

.article-card:hover .article-icon {
  transform: scale(1.2);
}

.article-category {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #1a1a1a;
}

.featured-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
}

.article-content {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.article-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: #6c757d;
  flex-wrap: wrap;
}

.dark-mode .article-meta {
  color: #a0a0a0;
}

.article-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #1a1a1a;
  line-height: 1.4;
}

.dark-mode .article-title {
  color: #ffffff;
}

.article-excerpt {
  color: #6c757d;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex: 1;
}

.dark-mode .article-excerpt {
  color: #a0a0a0;
}

.article-tags-preview {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.tag-mini {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.dark-mode .article-footer {
  border-top-color: rgba(255, 255, 255, 0.1);
}

.article-author {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.author-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
}

.author-name {
  font-weight: 600;
  color: #1a1a1a;
}

.dark-mode .author-name {
  color: #ffffff;
}

.read-more {
  color: #667eea;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.arrow {
  transition: transform 0.3s;
}

.article-card:hover .arrow {
  transform: translateX(-5px);
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
  flex-wrap: wrap;
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

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s ease-in;
}

.slide-fade-enter-from {
  transform: translateY(20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
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
  
  .articles-archive-grid {
    grid-template-columns: 1fr;
  }
  
  .article-image {
    height: 180px;
  }
  
  .article-icon {
    font-size: 3rem;
  }
  
  .pagination-pages {
    flex-wrap: wrap;
  }
}
</style>
