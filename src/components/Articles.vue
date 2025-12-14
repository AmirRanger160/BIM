<template>
  <section id="articles" class="articles-section">
    <Transition name="slide-fade">
      <ArticleDetail 
        v-if="selectedArticle" 
        :article="selectedArticle" 
        @close="closeArticle"
      />
    </Transition>
    
    <div v-show="!selectedArticle" class="container">
      <div class="section-header">
        <h2 class="section-title">آخرین مقالات</h2>
        <p class="section-subtitle">آموزش‌ها و اخبار روز دنیای تکنولوژی</p>
        <router-link v-if="showViewAll" to="/articles" class="view-all-btn">
          مشاهده همه مقالات
          <span class="btn-icon">→</span>
        </router-link>
      </div>
      
      <!-- Filters and Search -->
      <div class="articles-controls">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="جستجو در مقالات..."
            class="search-input"
          >
        </div>
        
        <div class="filter-tabs">
          <button 
            v-for="category in categories" 
            :key="category"
            @click="selectedCategory = category"
            class="filter-tab"
            :class="{ active: selectedCategory === category }"
          >
            <span class="filter-text">{{ category }}</span>
            <span v-if="selectedCategory === category" class="active-indicator"></span>
          </button>
        </div>
        
        <div class="sort-dropdown">
          <select v-model="sortBy" class="sort-select">
            <option value="latest">جدیدترین</option>
            <option value="popular">محبوب‌ترین</option>
            <option value="trending">پربازدیدترین</option>
          </select>
        </div>
      </div>
      
      <!-- Results Count -->
      <div class="results-info">
        <span class="results-count">{{ filteredArticles.length }} مقاله یافت شد</span>
      </div>
      
      <!-- Articles Grid -->
      <TransitionGroup name="articles-list" tag="div" class="articles-grid">
        <article 
          v-for="article in paginatedArticles" 
          :key="article.id" 
          class="article-card"
          @click="openArticle(article)"
        >
          <div class="article-image">
            <ImageSlider
              :image="article.image"
              :images="article.images"
              :icon="article.icon"
              :gradient="article.gradient"
            />
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
              <a href="#" class="read-more" @click.prevent>
                بیشتر
                <span class="arrow">←</span>
              </a>
            </div>
          </div>
        </article>
      </TransitionGroup>
      
      <!-- Load More / Pagination -->
      <div v-if="filteredArticles.length > articlesPerPage" class="pagination-section">
        <button 
          v-if="currentPage < totalPages"
          @click="loadMore" 
          class="load-more-btn"
        >
          مشاهده بیشتر
          <span class="btn-icon">⬇</span>
        </button>
        
        <div class="pagination-info">
          صفحه {{ currentPage }} از {{ totalPages }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import ArticleDetail from './ArticleDetail.vue'
import ImageSlider from './ImageSlider.vue'

const props = defineProps({
  showViewAll: {
    type: Boolean,
    default: false
  }
})

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
    fullContent: `
      <h2>مقدمه</h2>
      <p>دنیای طراحی وب همواره در حال تحول است. با پیشرفت تکنولوژی و تغییر انتظارات کاربران، طراحان و توسعه‌دهندگان باید همیشه در جریان آخرین روندها و تکنیک‌ها باشند.</p>
      
      <h3>۱. طراحی مینیمال و تمیز</h3>
      <p>یکی از مهم‌ترین ترندهای سال آینده، استفاده از طراحی‌های مینیمال و تمیز است. این روش به کاربران کمک می‌کند تا بدون حواس‌پرتی به محتوای اصلی توجه کنند.</p>
      
      <h3>۲. انیمیشن‌های روان</h3>
      <p>استفاده از انیمیشن‌های ظریف و هدفمند می‌تواند تجربه کاربری را بهبود بخشد. انیمیشن‌ها باید معنادار باشند و به راهنمایی کاربر کمک کنند.</p>
      
      <h3>۳. تم تاریک</h3>
      <p>حالت تاریک (Dark Mode) دیگر یک انتخاب اختیاری نیست، بلکه یک الزام است. کاربران انتظار دارند که بتوانند بین حالت روشن و تاریک جابجا شوند.</p>
      
      <h3>۴. طراحی ریسپانسیو پیشرفته</h3>
      <p>با تنوع دستگاه‌های موجود، طراحی ریسپانسیو باید فراتر از تنظیمات ساده برود و تجربه‌ای مناسب برای هر دستگاه فراهم کند.</p>
      
      <h2>نتیجه‌گیری</h2>
      <p>آینده طراحی وب متعلق به کسانی است که می‌توانند تکنولوژی را با خلاقیت ترکیب کنند و تجربه‌های بی‌نظیری برای کاربران خلق کنند.</p>
    `
  },
  {
    id: 2,
    title: 'بهینه‌سازی عملکرد وبسایت',
    excerpt: 'راهنمای کامل برای افزایش سرعت و بهینه‌سازی وبسایت‌های مدرن با تکنیک‌های پیشرفته.',
    date: '۱۲ دی ۱۴۰۴',
    readTime: '۸ دقیقه',
    category: 'توسعه',
    icon: '⚡',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    author: 'سارا رضایی',
    authorAvatar: 'س',
    authorRole: 'توسعه‌دهنده فرانت‌اند',
    views: '۳٫۲ هزار',
    viewsNum: 3200,
    featured: false,
    tags: ['عملکرد', 'بهینه‌سازی', 'سرعت', 'SEO'],
    fullContent: `
      <h2>چرا عملکرد مهم است؟</h2>
      <p>سرعت وبسایت یکی از مهم‌ترین عوامل در تجربه کاربری و رتبه‌بندی موتورهای جستجو است.</p>
    `
  },
  {
    id: 3,
    title: 'طراحی ریسپانسیو حرفه‌ای',
    excerpt: 'اصول و تکنیک‌های کلیدی برای ساخت وبسایت‌های سازگار با تمام دستگاه‌ها و اندازه صفحه‌ها.',
    date: '۱۰ دی ۱۴۰۴',
    readTime: '۶ دقیقه',
    category: 'موبایل',
    icon: '📱',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    author: 'علی کریمی',
    authorAvatar: 'ع',
    authorRole: 'توسعه‌دهنده فول‌استک',
    views: '۱٫۸ هزار',
    viewsNum: 1800,
    featured: false,
    tags: ['ریسپانسیو', 'موبایل', 'CSS', 'Media Queries'],
    fullContent: `
      <h2>اهمیت طراحی ریسپانسیو</h2>
      <p>با افزایش استفاده از دستگاه‌های موبایل، طراحی ریسپانسیو دیگر یک انتخاب نیست بلکه یک ضرورت است.</p>
    `
  },
  {
    id: 4,
    title: 'معماری مایکروسرویس‌ها',
    excerpt: 'راهنمای جامع برای طراحی و پیاده‌سازی معماری مایکروسرویس در پروژه‌های بزرگ و مقیاس‌پذیر.',
    date: '۸ دی ۱۴۰۴',
    readTime: '۱۲ دقیقه',
    category: 'توسعه',
    icon: '🏗️',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    author: 'رضا محمدی',
    authorAvatar: 'ر',
    authorRole: 'معمار نرم‌افزار',
    views: '۴٫۱ هزار',
    viewsNum: 4100,
    featured: true,
    tags: ['معماری', 'مایکروسرویس', 'Backend', 'Docker'],
    fullContent: `<h2>مقدمه</h2><p>معماری مایکروسرویس یک رویکرد نوین برای توسعه نرم‌افزار است.</p>`
  },
  {
    id: 5,
    title: 'امنیت در برنامه‌های وب',
    excerpt: 'بررسی تهدیدات رایج امنیتی و روش‌های محافظت از برنامه‌های وب در برابر حملات سایبری.',
    date: '۶ دی ۱۴۰۴',
    readTime: '۱۰ دقیقه',
    category: 'امنیت',
    icon: '🔒',
    gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    author: 'فاطمه کاظمی',
    authorAvatar: 'ف',
    authorRole: 'متخصص امنیت',
    views: '۲٫۹ هزار',
    viewsNum: 2900,
    featured: false,
    tags: ['امنیت', 'OWASP', 'حملات', 'محافظت'],
    fullContent: `<h2>امنیت اولویت اول است</h2><p>توجه به امنیت برنامه‌های وب از اهمیت ویژه‌ای برخوردار است.</p>`
  },
  {
    id: 6,
    title: 'React vs Vue: کدام یک را انتخاب کنیم؟',
    excerpt: 'مقایسه جامع دو فریم‌ورک محبوب React و Vue برای انتخاب بهترین گزینه در پروژه‌های مختلف.',
    date: '۴ دی ۱۴۰۴',
    readTime: '۷ دقیقه',
    category: 'طراحی',
    icon: '⚛️',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    author: 'امیر حسینی',
    authorAvatar: 'ا',
    authorRole: 'توسعه‌دهنده فرانت‌اند',
    views: '۵٫۳ هزار',
    viewsNum: 5300,
    featured: true,
    tags: ['React', 'Vue', 'فریم‌ورک', 'مقایسه'],
    fullContent: `<h2>مقدمه</h2><p>انتخاب بین React و Vue یکی از سوالات رایج است.</p>`
  }
])

const selectedArticle = ref(null)
const searchQuery = ref('')
const selectedCategory = ref('همه')
const sortBy = ref('latest')
const currentPage = ref(1)
const articlesPerPage = 6

const categories = computed(() => {
  const cats = ['همه', ...new Set(articles.value.map(a => a.category))]
  return cats
})

const filteredArticles = computed(() => {
  let filtered = articles.value
  
  if (selectedCategory.value !== 'همه') {
    filtered = filtered.filter(a => a.category === selectedCategory.value)
  }
  
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(a => 
      a.title.toLowerCase().includes(query) ||
      a.excerpt.toLowerCase().includes(query) ||
      a.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }
  
  if (sortBy.value === 'popular') {
    filtered = [...filtered].sort((a, b) => b.viewsNum - a.viewsNum)
  } else {
    filtered = [...filtered].sort((a, b) => b.id - a.id)
  }
  
  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredArticles.value.length / articlesPerPage)
})

const paginatedArticles = computed(() => {
  const end = currentPage.value * articlesPerPage
  const items = filteredArticles.value.slice(0, end)
  return props.showViewAll ? items.slice(0, 6) : items
})

const loadMore = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value = currentPage.value + 1
  }
}

const openArticle = (article) => {
  selectedArticle.value = article
}

const closeArticle = () => {
  selectedArticle.value = null
}
</script>

<style scoped>
.articles-section {
  padding: 6rem 0;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
  position: relative;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.dark-mode .section-title {
  color: #ffffff;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.dark-mode .section-subtitle {
  color: #a0a0a0;
}

.view-all-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.view-all-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-icon {
  transition: transform 0.3s ease;
}

.view-all-btn:hover .btn-icon {
  transform: translateX(5px);
}

.articles-controls {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
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
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  font-size: 1rem;
  background: white;
  transition: all 0.3s ease;
  font-family: inherit;
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

.filter-tab {
  padding: 0.5rem 1.5rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  background: white;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-size: 0.9rem;
  position: relative;
  overflow: hidden;
}

.filter-tab::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.filter-tab:hover::before {
  left: 100%;
}

.dark-mode .filter-tab {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.filter-text {
  position: relative;
  z-index: 1;
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

.filter-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.filter-tab:hover:not(.active) {
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.sort-dropdown {
  position: relative;
}

.sort-select {
  padding: 0.75rem 3rem 0.75rem 1.5rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  background: white;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  font-family: inherit;
  font-size: 0.9rem;
}

.dark-mode .sort-select {
  background-color: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.sort-select:focus {
  outline: none;
  border-color: #667eea;
}

.results-info {
  margin-bottom: 1.5rem;
  color: #6c757d;
  font-size: 0.95rem;
}

.dark-mode .results-info {
  color: #a0a0a0;
}

.results-count {
  font-weight: 600;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.article-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  cursor: pointer;
  position: relative;
}

.article-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: 0;
  pointer-events: none;
}

.article-card:hover::before {
  opacity: 1;
}

.dark-mode .article-card {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

.article-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 25px 50px rgba(102, 126, 234, 0.25), 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: rgba(102, 126, 234, 0.3);
}

.dark-mode .article-card:hover {
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 0 10px 20px rgba(102, 126, 234, 0.2);
}

.article-image {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  transition: all 0.5s ease;
}

.article-card:hover .article-image {
  transform: scale(1.1);
}

.article-image::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: rotate(45deg);
  transition: all 0.6s ease;
}

.article-card:hover .article-image::before {
  left: 100%;
}

@media (max-width: 640px) {
  .article-image {
    height: 180px;
  }
  
  .article-icon {
    font-size: 3rem;
  }
}

.article-icon {
  font-size: 4rem;
  position: relative;
  z-index: 1;
  transition: all 0.4s ease;
  filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.2));
}

.article-card:hover .article-icon {
  transform: scale(1.15) rotate(5deg);
  filter: drop-shadow(0 8px 20px rgba(0, 0, 0, 0.3));
}

.article-category {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.95);
  color: #1a1a1a;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  z-index: 2;
}

.article-card:hover .article-category {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.featured-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  color: #1a1a1a;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.8rem;
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
  transition: all 0.3s ease;
  animation: pulse-badge 2s ease-in-out infinite;
  z-index: 2;
}

@keyframes pulse-badge {
  0%, 100% {
    box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
  }
  50% {
    box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
  }
}

.article-card:hover .featured-badge {
  transform: scale(1.05);
}

.article-content {
  padding: 2rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

.article-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: #6c757d;
  flex-wrap: wrap;
}

.article-meta > span {
  transition: all 0.3s ease;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
}

.article-card:hover .article-meta > span {
  background: rgba(102, 126, 234, 0.05);
}

.dark-mode .article-meta {
  color: #a0a0a0;
}

.article-date::before {
  content: '📅 ';
}

.article-read-time::before {
  content: '⏱️ ';
}

.article-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1a1a1a;
  line-height: 1.4;
  transition: all 0.3s ease;
}

.dark-mode .article-title {
  color: #ffffff;
}

.article-card:hover .article-title {
  color: #667eea;
}

.article-excerpt {
  font-size: 1rem;
  line-height: 1.7;
  color: #6c757d;
  margin-bottom: 1rem;
  flex: 1;
}

.dark-mode .article-excerpt {
  color: #a0a0a0;
}

.article-tags-preview {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.tag-mini {
  padding: 0.25rem 0.75rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 50px;
  font-size: 0.75rem;
  color: #667eea;
  font-weight: 500;
  transition: all 0.3s ease;
}

.tag-mini:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
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
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.article-card:hover .author-avatar {
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
}

.author-name {
  font-size: 0.95rem;
  font-weight: 500;
  color: #1a1a1a;
  transition: all 0.3s ease;
}

.dark-mode .author-name {
  color: #ffffff;
}

.article-card:hover .author-name {
  color: #667eea;
}

.read-more {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  background: rgba(102, 126, 234, 0.1);
}

.read-more:hover {
  gap: 1rem;
  background: rgba(102, 126, 234, 0.2);
  transform: translateX(-3px);
}

.arrow {
  transition: transform 0.3s ease;
  display: inline-block;
}

.read-more:hover .arrow {
  transform: translateX(-5px);
  animation: arrow-bounce 0.6s ease-in-out infinite;
}

@keyframes arrow-bounce {
  0%, 100% {
    transform: translateX(-5px);
  }
  50% {
    transform: translateX(-10px);
  }
}

.pagination-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 3rem;
}

.load-more-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.load-more-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.load-more-btn:hover .btn-icon {
  transform: translateY(3px);
}

.pagination-info {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 500;
}

.dark-mode .pagination-info {
  color: #a0a0a0;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  transform: translateX(-20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

/* Articles List Transitions */
.articles-list-move,
.articles-list-enter-active,
.articles-list-leave-active {
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.articles-list-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(30px) rotateX(20deg);
}

.articles-list-leave-to {
  opacity: 0;
  transform: scale(0.8) translateY(-30px);
}

.articles-list-leave-active {
  position: absolute;
}

@media (max-width: 1024px) {
  .articles-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    min-width: 100%;
  }
  
  .filter-tabs {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .articles-section {
    padding: 4rem 0;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>
