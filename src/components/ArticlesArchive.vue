<template>
  <section class="articles-archive" id="articles">
    <div class="container">
      <h1 class="page-title animate-on-scroll">مقالات و اخبار</h1>
      
      <!-- Filters -->
      <div class="filters animate-on-scroll">
        <div class="filter-group">
          <label for="category-select">دسته‌بندی:</label>
          <select v-model="selectedCategory" id="category-select" @change="resetAndFetch">
            <option value="">تمام دسته‌بندی‌ها</option>
            <option value="BIM">BIM</option>
            <option value="Surveying">نقشه‌برداری</option>
            <option value="Technology">تکنولوژی</option>
            <option value="News">اخبار</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="search-input">جستجو:</label>
          <input v-model="searchQuery" id="search-input" type="text" placeholder="جستجو در مقالات..." @input="resetAndFetch">
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>درحال بارگذاری مقالات...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error">
        <p>{{ error }}</p>
      </div>

      <!-- Articles List -->
      <div v-else-if="filteredArticles.length > 0" class="articles-list">
        <article v-for="article in filteredArticles" :key="article.id" class="article-card animate-on-scroll">
          <div class="article-image">
            <img :src="article.image_url || 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 400 250%27%3E%3Crect fill=%27%23ddd%27 width=%27400%27 height=%27250%27/%3E%3C/svg%3E'" :alt="article.title_fa || article.title_en">
          </div>
          <div class="article-content">
            <div class="article-meta">
              <span class="category" v-if="article.category">{{ article.category }}</span>
              <span class="date">{{ formatDate(article.publish_date) }}</span>
            </div>
            <h2 class="article-title">{{ article.title_fa || article.title_en }}</h2>
            <p class="article-summary">{{ article.summary_fa || article.summary_en }}</p>
            <div class="article-tags" v-if="article.tags">
              <span class="tag" v-for="tag in article.tags.split(',')" :key="tag">
                {{ tag.trim() }}
              </span>
            </div>
            <a href="#" @click.prevent="navigateTo(`/article/${article.slug || article.id}`)" class="btn-read-more">مطالعه بیشتر</a>
          </div>
        </article>
      </div>

      <!-- No Articles -->
      <div v-else class="no-articles">
        <p>هیچ مقاله‌ای یافت نشد.</p>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button 
          :disabled="currentPage === 1"
          @click="previousPage"
          class="btn-page"
        >
          صفحه قبلی
        </button>
        
        <span class="page-info">
          صفحه {{ currentPage }} از {{ totalPages }}
        </span>
        
        <button 
          :disabled="currentPage === totalPages"
          @click="nextPage"
          class="btn-page"
        >
          صفحه بعدی
        </button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ArticlesArchive',
  inject: ['navigateTo'],
  data() {
    return {
      articles: [],
      filteredArticles: [],
      loading: false,
      error: null,
      currentPage: 1,
      itemsPerPage: 6,
      selectedCategory: '',
      searchQuery: '',
      totalPages: 1
    }
  },
  mounted() {
    this.fetchArticles();
    // Ensure elements are visible when component mounts
    this.$nextTick(() => {
      setTimeout(() => {
        const elements = this.$el.querySelectorAll('.animate-on-scroll');
        elements.forEach(el => el.classList.add('in-view'));
      }, 50);
    });
  },
  methods: {
    async fetchArticles() {
      this.loading = true;
      this.error = null;
      try {
        // Sample data - replace with API call
        this.articles = [
          {
            id: 1,
            slug: 'bim-benefits-2024',
            title_en: 'Benefits of BIM Technology in Modern Construction',
            title_fa: 'فوایدی فناوری BIM در ساخت و ساز مدرن',
            summary_en: 'Explore how BIM technology is revolutionizing the construction industry.',
            summary_fa: 'کاوش کنید که چگونه فناوری BIM صنعت ساخت و ساز را متحول می‌کند.',
            content_en: 'BIM (Building Information Modeling) has become an essential tool...',
            content_fa: 'BIM (مدل‌سازی اطلاعات ساختمان) به ابزاری ضروری تبدیل شده است...',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 400 250%27%3E%3Crect fill=%27%231abc9c%27 width=%27400%27 height=%27250%27/%3E%3C/svg%3E',
            category: 'BIM',
            tags: 'BIM, Construction, Technology',
            author: 'GeoBiro Team',
            publish_date: '2025-01-15T10:00:00'
          },
          {
            id: 2,
            slug: 'laser-scanning-guide',
            title_en: 'Complete Guide to Laser Scanning and Point Clouds',
            title_fa: 'راهنمای کامل اسکن لیزری و ابر نقاط',
            summary_en: 'Learn about the latest laser scanning techniques and their applications.',
            summary_fa: 'درباره آخرین تکنیک‌های اسکن لیزری و کاربردهای آن بیاموزید.',
            content_en: 'Laser scanning technology has revolutionized surveying...',
            content_fa: 'فناوری اسکن لیزری نقشه‌برداری را متحول کرده است...',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 400 250%27%3E%3Crect fill=%27%232d5f3f%27 width=%27400%27 height=%27250%27/%3E%3C/svg%3E',
            category: 'Surveying',
            tags: 'Laser Scanning, Point Cloud, Technology',
            author: 'GeoBiro Team',
            publish_date: '2025-01-10T10:00:00'
          },
          {
            id: 3,
            slug: 'digital-twin-technology',
            title_en: 'Digital Twin Technology in Real Estate',
            title_fa: 'فناوری دیجیتال دوقلو در املاک و مستغلات',
            summary_en: 'How digital twins are transforming property management.',
            summary_fa: 'چگونه دوقلوهای دیجیتالی مدیریت اموال را تغییر می‌دهند.',
            content_en: 'Digital twin technology creates virtual replicas...',
            content_fa: 'فناوری دوقلو دیجیتالی نسخه‌های مجازی ایجاد می‌کند...',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 400 250%27%3E%3Crect fill=%27%23333%27 width=%27400%27 height=%27250%27/%3E%3C/svg%3E',
            category: 'Technology',
            tags: 'Digital Twin, Real Estate, Innovation',
            author: 'GeoBiro Team',
            publish_date: '2025-01-05T10:00:00'
          },
          {
            id: 4,
            slug: 'surveying-standards-2024',
            title_en: 'New Surveying Standards in 2024',
            title_fa: 'استانداردهای نقشه‌برداری جدید در سال ۲۰۲۴',
            summary_en: 'Updates on international surveying standards and regulations.',
            summary_fa: 'به‌روزرسانی‌های استانداردها و مقررات نقشه‌برداری بین‌المللی.',
            content_en: 'The surveying industry has adopted new standards...',
            content_fa: 'صنعت نقشه‌برداری استانداردهای جدیدی پذیرفته است...',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 400 250%27%3E%3Crect fill=%27%234a7c59%27 width=%27400%27 height=%27250%27/%3E%3C/svg%3E',
            category: 'News',
            tags: 'Standards, Surveying, Regulations',
            author: 'GeoBiro Team',
            publish_date: '2024-12-28T10:00:00'
          },
          {
            id: 5,
            slug: 'bim-software-comparison',
            title_en: 'BIM Software Comparison: Revit vs ArchiCAD',
            title_fa: 'مقایسه نرم‌افزار BIM: Revit در برابر ArchiCAD',
            summary_en: 'In-depth comparison of popular BIM software solutions.',
            summary_fa: 'مقایسه عمیق راه‌حل‌های نرم‌افزار BIM محبوب.',
            content_en: 'Choosing the right BIM software is crucial...',
            content_fa: 'انتخاب نرم‌افزار BIM مناسب حیاتی است...',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 400 250%27%3E%3Crect fill=%27%235a8c6e%27 width=%27400%27 height=%27250%27/%3E%3C/svg%3E',
            category: 'BIM',
            tags: 'BIM, Revit, ArchiCAD, Comparison',
            author: 'GeoBiro Team',
            publish_date: '2024-12-20T10:00:00'
          },
          {
            id: 6,
            slug: 'portfolio-new-projects',
            title_en: 'New Projects Added to Our Portfolio',
            title_fa: 'پروژه‌های جدید به پورتفولیو ما اضافه شدند',
            summary_en: 'Check out our latest completed projects and case studies.',
            summary_fa: 'آخرین پروژه‌های تکمیل‌شده و مطالعات موردی ما را بررسی کنید.',
            content_en: 'We are proud to announce several new projects...',
            content_fa: 'ما افتخار می‌کنیم که چندین پروژه جدید را اعلام کنیم...',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 400 250%27%3E%3Crect fill=%27%236a5a3e%27 width=%27400%27 height=%27250%27/%3E%3C/svg%3E',
            category: 'News',
            tags: 'Projects, Portfolio, Case Studies',
            author: 'GeoBiro Team',
            publish_date: '2024-12-15T10:00:00'
          }
        ];
        
        this.filterAndPaginate();
      } catch (err) {
        this.error = 'خطا در بارگذاری مقالات';
        console.error('Error fetching articles:', err);
      } finally {
        this.loading = false;
      }
    },
    filterAndPaginate() {
      let filtered = this.articles;

      // Filter by category
      if (this.selectedCategory) {
        filtered = filtered.filter(a => a.category === this.selectedCategory);
      }

      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(a => 
          (a.title_fa && a.title_fa.includes(this.searchQuery)) ||
          (a.title_en && a.title_en.toLowerCase().includes(query)) ||
          (a.summary_fa && a.summary_fa.includes(this.searchQuery)) ||
          (a.summary_en && a.summary_en.toLowerCase().includes(query))
        );
      }

      // Calculate pagination
      this.totalPages = Math.ceil(filtered.length / this.itemsPerPage);
      if (this.currentPage > this.totalPages && this.totalPages > 0) {
        this.currentPage = this.totalPages;
      }

      // Apply pagination
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      this.filteredArticles = filtered.slice(start, end);
    },
    resetAndFetch() {
      this.currentPage = 1;
      this.filterAndPaginate();
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.filterAndPaginate();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.filterAndPaginate();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('fa-IR', options);
    }
  }
}
</script>

<style scoped>
.articles-archive {
  padding: 60px 50px;
  background: #ffffff;
  min-height: 100vh;
}

.container {
  max-width: 1000px;
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
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 50px;
  padding: 25px;
  background: #f9f9f9;
  border: 1px solid #e8e8e8;
  text-align: right;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.filter-group select,
.filter-group input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 2px;
  font-size: 14px;
  direction: rtl;
  text-align: right;
}

.filter-group select:focus,
.filter-group input:focus {
  outline: none;
  border-color: #1abc9c;
  box-shadow: 0 0 0 2px rgba(26, 188, 156, 0.1);
}

/* Articles List */
.articles-list {
  display: grid;
  gap: 35px;
  margin-bottom: 50px;
}

.article-card {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 30px;
  padding: 0;
  background: #ffffff;
  border: 1px solid #e8e8e8;
  transition: all 0.3s ease-out;
}

.article-card:hover {
  border-color: #1abc9c;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.article-image {
  width: 300px;
  height: 200px;
  overflow: hidden;
  background: #f5f5f5;
}

.article-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease-out;
}

.article-card:hover .article-image img {
  transform: scale(1.05);
}

.article-content {
  padding: 25px;
  text-align: right;
  display: flex;
  flex-direction: column;
}

.article-meta {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-bottom: 12px;
  font-size: 13px;
}

.category {
  background: #1abc9c;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 600;
}

.date {
  color: #999;
}

.article-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #1a1a1a;
  line-height: 1.4;
}

.article-summary {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
  margin-bottom: 15px;
  flex-grow: 1;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 8px;
  margin-bottom: 15px;
}

.tag {
  background: #f0f0f0;
  color: #555;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.btn-read-more {
  align-self: flex-start;
  padding: 10px 20px;
  background: #1abc9c;
  color: white;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  border: none;
  border-radius: 2px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-read-more:hover {
  background: #16a085;
  transform: scale(1.02);
}

/* Loading & Error States */
.loading, .error, .no-articles {
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

.no-articles {
  color: #999;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 50px;
}

.btn-page {
  padding: 10px 20px;
  background: #1abc9c;
  color: white;
  border: none;
  border-radius: 2px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease-out;
}

.btn-page:hover:not(:disabled) {
  background: #16a085;
  transform: scale(1.02);
}

.btn-page:disabled {
  background: #ddd;
  cursor: not-allowed;
  opacity: 0.5;
}

.page-info {
  color: #666;
  font-size: 14px;
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
@media (max-width: 768px) {
  .articles-archive {
    padding: 30px 20px;
  }

  .page-title {
    font-size: 24px;
    margin-bottom: 30px;
  }

  .filters {
    grid-template-columns: 1fr;
    gap: 15px;
    padding: 20px;
  }

  .article-card {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .article-image {
    width: 100%;
    height: 200px;
  }

  .article-content {
    padding: 20px;
  }

  .article-title {
    font-size: 18px;
  }

  .article-meta {
    justify-content: flex-end;
    gap: 10px;
  }

  .pagination {
    gap: 10px;
    flex-wrap: wrap;
  }

  .btn-page {
    padding: 8px 16px;
    font-size: 13px;
  }
}
</style>
