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
import { articleService } from '../services/api';

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
        const response = await articleService.getAll({ skip: 0, limit: 100, is_published: true });
        this.articles = response.data;
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

.filter-group select,
.filter-group input {
  padding: 8px 10px;
  border: none;
  border-bottom: 1px solid #ddd;
  font-size: 13px;
  direction: rtl;
  text-align: right;
  background: transparent;
  min-width: 150px;
}

.filter-group select:focus,
.filter-group input:focus {
  outline: none;
  border-bottom-color: #1abc9c;
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
  transition: all 0.3s ease-out;
}

.article-card:hover {
  transform: translateY(-2px);
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
