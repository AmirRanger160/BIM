<template>
  <section class="featured-articles-section" id="featured-articles">
    <h2 class="section-title animate-on-scroll">مقالات و اخبار</h2>
    <div class="articles-grid">
      <article class="article-card animate-on-scroll" v-for="(article, index) in articles" :key="article.id">
        <div class="article-image">
          <img :src="article.image_url || 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 200%27%3E%3Crect fill=%27%23ddd%27 width=%27300%27 height=%27200%27/%3E%3C/svg%3E'" :alt="article.title_fa || article.title_en">
          <span class="article-category" v-if="article.category">{{ article.category }}</span>
        </div>
        <div class="article-content">
          <h3>{{ article.title_fa || article.title_en }}</h3>
          <p class="article-summary">{{ article.summary_fa || article.summary_en }}</p>
          <div class="article-meta">
            <span class="article-date">{{ new Date(article.publish_date).toLocaleDateString('fa-IR', { year: 'numeric', month: 'long', day: 'numeric' }) }}</span>
            <a href="#" @click.prevent="navigateTo(`/article/${article.slug || article.id}`)" class="btn-read-more">مطالعه بیشتر</a>
          </div>
        </div>
      </article>
    </div>
    
    <!-- View All Articles Button -->
    <div class="view-all-button">
      <a href="#" @click.prevent="navigateTo('/articles')" class="btn-view-all">مشاهده تمام مقالات</a>
    </div>
  </section>
</template>

<script>
import { articleService } from '../services/api';

export default {
  name: 'FeaturedArticles',
  inject: ['navigateTo'],
  data() {
    return {
      articles: [],
      loading: false,
      error: null
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
        const response = await articleService.getAll({ skip: 0, limit: 3, is_published: true });
        this.articles = response.data.slice(0, 3);
      } catch (err) {
        this.error = 'خطا در بارگذاری مقالات';
        console.error('Error fetching articles:', err);
        this.articles = [];
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.featured-articles-section {
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
  margin-bottom: 20px;
  color: #1a1a1a;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 25px;
  width: 100%;
  max-width: 1200px;
  margin-top: 25px;
  margin-bottom: 0;
}

.article-card {
  background: #ffffff;
  cursor: pointer;
  transition: all 0.3s ease-out;
  text-align: right;
  overflow: hidden;
}

.article-card:hover {
  transform: translateY(-4px);
}

.article-image {
  position: relative;
  width: 100%;
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

.article-category {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #1abc9c;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.article-content {
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.article-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #1a1a1a;
  word-wrap: break-word;
  word-break: break-word;
  line-height: 1.4;
}

.article-summary {
  font-size: 13px;
  line-height: 1.6;
  color: #666666;
  margin-bottom: 15px;
  flex-grow: 1;
  min-height: 40px;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.article-date {
  font-size: 12px;
  color: #999;
}

.btn-read-more {
  display: inline-block;
  padding: 8px 16px;
  background: transparent;
  color: #666;
  text-decoration: none;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 2px;
}

.btn-read-more:hover {
  background: #f5f5f5;
  border-color: #999;
  transform: scale(1.02);
}

/* View All Button */
.view-all-button {
  text-align: center;
  margin-top: 50px;
  width: 100%;
  max-width: 1200px;
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
  border-color: #666;
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
  .articles-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .featured-articles-section {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .articles-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 30px;
  }

  .featured-articles-section {
    padding: 30px 20px;
  }

  .article-image {
    height: 180px;
  }

  .article-content {
    padding: 20px;
  }

  .article-card h3 {
    font-size: 16px;
    margin-bottom: 10px;
  }

  .article-summary {
    font-size: 12px;
    min-height: 35px;
  }
}
</style>
