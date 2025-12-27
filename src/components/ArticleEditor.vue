<template>
  <div class="article-editor-wrapper">
    <!-- Article Form -->
    <div class="article-form-section">
      <h2>{{ editingArticle ? 'ویرایش مقاله' : 'ایجاد مقاله جدید' }}</h2>
      <AdminForm
        contentType="articles"
        :item="editingArticle"
        @save="saveArticle"
        @cancel="cancelEdit"
      />
    </div>

    <!-- Image Manager (only show when editing an existing article) -->
    <div v-if="editingArticle && editingArticle.id" class="image-manager-section">
      <ArticleImageManager :articleId="editingArticle.id" />
    </div>

    <!-- Message when creating new article -->
    <div v-else class="info-message">
      <p>⚠️ برای افزودن تصاویر، ابتدا مقاله را ایجاد کنید.</p>
    </div>
  </div>
</template>

<script>
import AdminForm from './AdminForm.vue';
import ArticleImageManager from './ArticleImageManager.vue';

export default {
  name: 'ArticleEditor',
  components: {
    AdminForm,
    ArticleImageManager
  },
  props: {
    article: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      editingArticle: null
    }
  },
  watch: {
    article: {
      handler(newVal) {
        this.editingArticle = newVal;
      },
      immediate: true
    }
  },
  methods: {
    async saveArticle(articleData) {
      this.$emit('save', articleData);
    },
    cancelEdit() {
      this.$emit('cancel');
    }
  }
}
</script>

<style scoped>
.article-editor-wrapper {
  display: grid;
  gap: 30px;
}

.article-form-section {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.article-form-section h2 {
  margin-top: 0;
  margin-bottom: 25px;
  color: #333;
  font-size: 20px;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 15px;
}

.image-manager-section {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.info-message {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 6px;
  padding: 15px;
  color: #856404;
  text-align: center;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .article-editor-wrapper {
    gap: 20px;
  }

  .article-form-section,
  .image-manager-section {
    padding: 15px;
  }
}
</style>
