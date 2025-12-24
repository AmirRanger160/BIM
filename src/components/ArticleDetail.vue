<template>
  <section class="article-detail" id="article-detail">
    <div class="container">
      <!-- Back Button -->
      <a href="#" @click.prevent="navigateTo('/articles')" class="btn-back">← بازگشت به مقالات</a>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>درحال بارگذاری مقاله...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="error">
        <p>{{ error }}</p>
        <a href="#" @click.prevent="navigateTo('/articles')" class="btn-back">بازگشت به مقالات</a>
      </div>

      <!-- Article Content -->
      <article v-else-if="article" class="article-content">
        <!-- Meta Information -->
        <div class="article-meta">
          <span class="category" v-if="article.category">{{ article.category }}</span>
          <span class="author" v-if="article.author">نوشتار: {{ article.author }}</span>
          <span class="date">{{ formatDate(article.publish_date) }}</span>
        </div>

        <!-- Title -->
        <h1 class="article-title">{{ article.title_fa || article.title_en }}</h1>

        <!-- Featured Image -->
        <div class="article-featured-image">
          <img :src="article.image_url || 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 800 400%27%3E%3Crect fill=%27%23ddd%27 width=%27800%27 height=%27400%27/%3E%3C/svg%3E'" :alt="article.title_fa || article.title_en">
        </div>

        <!-- Summary -->
        <div class="article-summary">
          <p>{{ article.summary_fa || article.summary_en }}</p>
        </div>

        <!-- Tags -->
        <div class="article-tags" v-if="article.tags">
          <span class="tag" v-for="tag in article.tags.split(',')" :key="tag">
            #{{ tag.trim() }}
          </span>
        </div>

        <!-- Main Content -->
        <div class="article-body" v-html="article.content_fa || article.content_en"></div>

        <!-- Sharing Section -->
        <div class="article-sharing">
          <h3>اشتراک‌گذاری این مقاله:</h3>
          <div class="share-buttons">
            <button @click="shareArticle('twitter')" class="share-btn twitter">Twitter</button>
            <button @click="shareArticle('facebook')" class="share-btn facebook">Facebook</button>
            <button @click="shareArticle('linkedin')" class="share-btn linkedin">LinkedIn</button>
            <button @click="copyLink" class="share-btn copy">کپی لینک</button>
          </div>
        </div>

        <!-- Related Articles -->
        <div class="related-articles" v-if="relatedArticles.length > 0">
          <h3>مقالات مرتبط:</h3>
          <div class="related-grid">
            <a v-for="related in relatedArticles" :key="related.id" href="#" @click.prevent="navigateTo(`/article/${related.slug || related.id}`)" class="related-card">
              <img :src="related.image_url || 'data:image/svg+xml/%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 200%27%3E%3Crect fill=%27%23ddd%27 width=%27300%27 height=%27200%27/%3E%3C/svg%3E'" :alt="related.title_fa || related.title_en">
              <h4>{{ related.title_fa || related.title_en }}</h4>
            </a>
          </div>
        </div>
      </article>

      <!-- 404 Not Found -->
      <div v-else-if="!loading && !error" class="not-found">
        <p>مقاله مورد نظر یافت نشد.</p>
        <a href="#" @click.prevent="navigateTo('/articles')" class="btn-back">بازگشت به مقالات</a>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ArticleDetail',
  inject: ['navigateTo'],
  data() {
    return {
      article: null,
      articles: [],
      relatedArticles: [],
      loading: false,
      error: null,
      articleId: null
    }
  },
  watch: {
    $route: {
      handler() {
        this.loadArticle();
      },
      immediate: true
    }
  },
  mounted() {
    this.loadArticle();
    // Initialize animations observer if needed
    this.$nextTick(() => {
      if (this.$parent && this.$parent.initIntersectionObserver) {
        this.$parent.initIntersectionObserver();
      }
    });
  },
  methods: {
    loadArticle() {
      // Extract article ID/slug from URL pathname
      const pathname = window.location.pathname;
      const match = pathname.match(/\/article\/(.+)/);
      this.articleId = match ? decodeURIComponent(match[1]) : null;

      if (this.articleId) {
        this.fetchArticle();
      }
    },
    async fetchArticle() {
      this.loading = true;
      this.error = null;
      try {
        // Sample data - replace with API call
        const allArticles = [
          {
            id: 1,
            slug: 'bim-benefits-2024',
            title_en: 'Benefits of BIM Technology in Modern Construction',
            title_fa: 'فوایدی فناوری BIM در ساخت و ساز مدرن',
            summary_en: 'Explore how BIM technology is revolutionizing the construction industry.',
            summary_fa: 'کاوش کنید که چگونه فناوری BIM صنعت ساخت و ساز را متحول می‌کند.',
            content_en: '<h2>What is BIM?</h2><p>Building Information Modeling (BIM) is a digital representation of the physical and functional characteristics of a building. It serves as a shared knowledge resource for information about a facility, forming a reliable basis for decisions during its life cycle...</p><h2>Key Benefits</h2><p>BIM technology offers numerous advantages including improved collaboration, better visualization, reduced costs, and enhanced project delivery...</p>',
            content_fa: '<h2>BIM چیست؟</h2><p>مدل‌سازی اطلاعات ساختمان (BIM) نمایش دیجیتالی از ویژگی‌های فیزیکی و عملکردی یک ساختمان است. این به عنوان یک منبع دانش مشترک برای اطلاعات درباره یک تاسیسات عمل می‌کند...</p><h2>فوایدی اصلی</h2><p>فناوری BIM مزایای متعددی از جمله همکاری بهتر، بصری‌سازی بهتر، کاهش هزینه‌ها و تحویل پروژه بهتر ارائه می‌دهد...</p>',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 800 400%27%3E%3Crect fill=%27%231abc9c%27 width=%27800%27 height=%27400%27/%3E%3C/svg%3E',
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
            content_en: '<h2>Introduction to Laser Scanning</h2><p>Laser scanning technology has revolutionized the surveying industry by providing accurate and detailed 3D information about objects and environments...</p>',
            content_fa: '<h2>مقدمه‌ای بر اسکن لیزری</h2><p>فناوری اسکن لیزری صنعت نقشه‌برداری را با ارائه اطلاعات سه‌بعدی دقیق و جزئی درباره اشیاء و محیط‌ها متحول کرده است...</p>',
            image_url: 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 800 400%27%3E%3Crect fill=%27%232d5f3f%27 width=%27800%27 height=%27400%27/%3E%3C/svg%3E',
            category: 'Surveying',
            tags: 'Laser Scanning, Point Cloud',
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
            content_en: '<p>Digital twin technology...</p>',
            content_fa: '<p>فناوری دوقلو دیجیتالی...</p>',
            image_url: 'data:image/svg+xml/%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 800 400%27%3E%3Crect fill=%27%23333%27 width=%27800%27 height=%27400%27/%3E%3C/svg%3E',
            category: 'Technology',
            tags: 'Digital Twin, Real Estate',
            author: 'GeoBiro Team',
            publish_date: '2025-01-05T10:00:00'
          }
        ];

        // Find article by ID or slug
        this.article = allArticles.find(a => 
          a.id == this.articleId || a.slug === this.articleId
        );

        if (!this.article) {
          this.error = 'مقاله مورد نظر یافت نشد.';
          return;
        }

        // Get related articles (same category, different article)
        this.relatedArticles = allArticles
          .filter(a => a.category === this.article.category && a.id !== this.article.id)
          .slice(0, 3);

      } catch (err) {
        this.error = 'خطا در بارگذاری مقاله';
        console.error('Error fetching article:', err);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('fa-IR', options);
    },
    shareArticle(platform) {
      const url = window.location.href;
      const title = this.article.title_fa || this.article.title_en;
      
      const shareUrls = {
        twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`,
        facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
        linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`
      };

      if (shareUrls[platform]) {
        window.open(shareUrls[platform], '_blank', 'width=600,height=400');
      }
    },
    copyLink() {
      const url = window.location.href;
      navigator.clipboard.writeText(url).then(() => {
        alert('لینک کپی شد!');
      });
    }
  }
}
</script>

<style scoped>
.article-detail {
  padding: 60px 50px;
  background: #ffffff;
  min-height: 100vh;
}

.container {
  max-width: 800px;
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

.error .btn-back {
  display: block;
  margin-top: 20px;
}

/* Article Meta */
.article-meta {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  margin-bottom: 20px;
  font-size: 13px;
  flex-wrap: wrap;
  text-align: right;
}

.category {
  background: #1abc9c;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 600;
}

.author, .date {
  color: #666;
}

/* Article Title */
.article-title {
  font-size: 38px;
  font-weight: bold;
  line-height: 1.3;
  margin-bottom: 30px;
  color: #1a1a1a;
  text-align: right;
}

/* Featured Image */
.article-featured-image {
  width: 100%;
  height: 400px;
  margin-bottom: 40px;
  overflow: hidden;
  border-radius: 2px;
  background: #f5f5f5;
}

.article-featured-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Summary */
.article-summary {
  font-size: 16px;
  line-height: 1.8;
  color: #555;
  margin-bottom: 30px;
  padding: 20px;
  background: #f9f9f9;
  border-right: 3px solid #1abc9c;
  text-align: right;
}

/* Tags */
.article-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
  margin-bottom: 40px;
}

.tag {
  background: #f0f0f0;
  color: #555;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
}

/* Article Body */
.article-body {
  font-size: 15px;
  line-height: 1.8;
  color: #333;
  margin-bottom: 50px;
  text-align: right;
}

.article-body h2 {
  font-size: 24px;
  font-weight: bold;
  margin-top: 30px;
  margin-bottom: 15px;
  color: #1a1a1a;
}

.article-body h3 {
  font-size: 18px;
  font-weight: 600;
  margin-top: 25px;
  margin-bottom: 12px;
  color: #333;
}

.article-body p {
  margin-bottom: 15px;
  line-height: 1.8;
}

.article-body ul, .article-body ol {
  margin: 20px 0;
  padding-right: 20px;
}

.article-body li {
  margin-bottom: 8px;
  line-height: 1.8;
}

/* Sharing Section */
.article-sharing {
  padding: 30px;
  background: #f9f9f9;
  border: 1px solid #e8e8e8;
  margin-bottom: 50px;
  text-align: right;
}

.article-sharing h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #1a1a1a;
}

.share-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
}

.share-btn {
  padding: 10px 16px;
  border: none;
  border-radius: 2px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s ease-out;
}

.share-btn.twitter {
  background: #1DA1F2;
}

.share-btn.facebook {
  background: #1877F2;
}

.share-btn.linkedin {
  background: #0A66C2;
}

.share-btn.copy {
  background: #666;
}

.share-btn:hover {
  transform: scale(1.05);
  opacity: 0.9;
}

/* Related Articles */
.related-articles {
  margin-top: 50px;
  text-align: right;
}

.related-articles h3 {
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
}

.related-card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
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
  .article-detail {
    padding: 30px 20px;
  }

  .article-title {
    font-size: 28px;
  }

  .article-featured-image {
    height: 250px;
  }

  .article-meta {
    justify-content: flex-end;
    gap: 12px;
  }

  .article-body {
    font-size: 14px;
  }

  .article-body h2 {
    font-size: 20px;
  }

  .article-body h3 {
    font-size: 16px;
  }

  .share-buttons {
    justify-content: flex-end;
    gap: 8px;
  }

  .share-btn {
    padding: 8px 12px;
    font-size: 12px;
  }

  .related-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}
</style>
