<template>
  <div class="article-image-manager">
    <div class="image-manager-header">
      <h3>مدیریت تصاویر مقاله</h3>
      <button @click="showUploadForm = !showUploadForm" class="btn-add-image">
        {{ showUploadForm ? '❌ بستن' : '➕ افزودن تصویر' }}
      </button>
    </div>

    <!-- Upload Form -->
    <div v-if="showUploadForm" class="upload-form">
      <div class="form-group">
        <label for="image-url">URL تصویر:</label>
        <input 
          v-model="newImage.image_url" 
          type="text" 
          id="image-url"
          placeholder="https://example.com/image.jpg"
          class="input-field"
        >
      </div>

      <div class="form-group">
        <label for="caption-en">توضیح (انگلیسی):</label>
        <textarea 
          v-model="newImage.caption_en" 
          id="caption-en"
          placeholder="English caption..."
          class="input-field"
          rows="2"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="caption-fa">توضیح (فارسی):</label>
        <textarea 
          v-model="newImage.caption_fa" 
          id="caption-fa"
          placeholder="توضیح فارسی..."
          class="input-field"
          rows="2"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="alt-text-en">متن alt (انگلیسی):</label>
        <input 
          v-model="newImage.alt_text_en" 
          type="text" 
          id="alt-text-en"
          placeholder="Image description in English"
          class="input-field"
        >
      </div>

      <div class="form-group">
        <label for="alt-text-fa">متن alt (فارسی):</label>
        <input 
          v-model="newImage.alt_text_fa" 
          type="text" 
          id="alt-text-fa"
          placeholder="توضیح تصویر"
          class="input-field"
        >
      </div>

      <button @click="uploadImage" class="btn-submit" :disabled="!newImage.image_url">
        {{ uploading ? 'در حال بارگذاری...' : 'بارگذاری تصویر' }}
      </button>
    </div>

    <!-- Images List -->
    <div v-if="images.length > 0" class="images-list">
      <div 
        v-for="(image, index) in images" 
        :key="image.id" 
        class="image-card"
        draggable="true"
        @dragstart="dragStart(index)"
        @dragover.prevent="dragOver(index)"
        @drop="dragDrop(index)"
        @dragend="dragEnd"
      >
        <div class="image-preview">
          <img :src="image.image_url" :alt="image.alt_text_fa || image.alt_text_en" />
          <span class="drag-indicator">⋮⋮</span>
        </div>

        <div class="image-info">
          <div class="image-captions">
            <p v-if="image.caption_fa" class="caption-fa"><strong>فارسی:</strong> {{ image.caption_fa }}</p>
            <p v-if="image.caption_en" class="caption-en"><strong>English:</strong> {{ image.caption_en }}</p>
          </div>

          <div class="image-actions">
            <button @click="deleteImage(image.id)" class="btn-delete">🗑️ حذف</button>
            <button @click="editImage(image)" class="btn-edit">✏️ ویرایش</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <p>هیچ تصویری برای این مقاله درج نشده است.</p>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingImage" class="edit-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>ویرایش تصویر</h3>
          <button @click="editingImage = null" class="close-btn">✕</button>
        </div>

        <div class="form-group">
          <label>URL تصویر:</label>
          <input 
            v-model="editingImage.image_url" 
            type="text"
            class="input-field"
          >
        </div>

        <div class="form-group">
          <label>توضیح (فارسی):</label>
          <textarea 
            v-model="editingImage.caption_fa"
            class="input-field"
            rows="2"
          ></textarea>
        </div>

        <div class="form-group">
          <label>توضیح (انگلیسی):</label>
          <textarea 
            v-model="editingImage.caption_en"
            class="input-field"
            rows="2"
          ></textarea>
        </div>

        <div class="modal-actions">
          <button @click="saveEditedImage" class="btn-save">💾 ذخیره</button>
          <button @click="editingImage = null" class="btn-cancel">لغو</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { articleService } from '../services/api';

export default {
  name: 'ArticleImageManager',
  props: {
    articleId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      images: [],
      newImage: {
        image_url: '',
        caption_en: '',
        caption_fa: '',
        alt_text_en: '',
        alt_text_fa: ''
      },
      editingImage: null,
      showUploadForm: false,
      uploading: false,
      draggedIndex: null
    }
  },
  mounted() {
    this.loadImages();
  },
  methods: {
    async loadImages() {
      try {
        const response = await articleService.getImages(this.articleId);
        this.images = response.data || [];
      } catch (error) {
        console.error('خطا در بارگذاری تصاویر:', error);
      }
    },

    async uploadImage() {
      if (!this.newImage.image_url.trim()) {
        alert('لطفا URL تصویر را وارد کنید');
        return;
      }

      this.uploading = true;
      try {
        const imageData = {
          ...this.newImage,
          order: this.images.length
        };

        await articleService.addImage(this.articleId, imageData);
        
        // Reset form
        this.newImage = {
          image_url: '',
          caption_en: '',
          caption_fa: '',
          alt_text_en: '',
          alt_text_fa: ''
        };
        this.showUploadForm = false;

        // Reload images
        await this.loadImages();
        
        alert('تصویر با موفقیت افزوده شد');
      } catch (error) {
        console.error('خطا در بارگذاری تصویر:', error);
        alert('خطا در بارگذاری تصویر');
      } finally {
        this.uploading = false;
      }
    },

    async deleteImage(imageId) {
      if (!confirm('آیا از حذف این تصویر اطمینان دارید؟')) {
        return;
      }

      try {
        await articleService.deleteImage(this.articleId, imageId);
        await this.loadImages();
        alert('تصویر با موفقیت حذف شد');
      } catch (error) {
        console.error('خطا در حذف تصویر:', error);
        alert('خطا در حذف تصویر');
      }
    },

    editImage(image) {
      this.editingImage = { ...image };
    },

    async saveEditedImage() {
      try {
        await articleService.updateImage(
          this.articleId,
          this.editingImage.id,
          this.editingImage
        );
        this.editingImage = null;
        await this.loadImages();
        alert('تصویر با موفقیت ویرایش شد');
      } catch (error) {
        console.error('خطا در ویرایش تصویر:', error);
        alert('خطا در ویرایش تصویر');
      }
    },

    dragStart(index) {
      this.draggedIndex = index;
    },

    dragOver(index) {
      // Visual feedback during drag
    },

    dragDrop(index) {
      if (this.draggedIndex !== null && this.draggedIndex !== index) {
        const draggedImage = this.images[this.draggedIndex];
        this.images.splice(this.draggedIndex, 1);
        this.images.splice(index, 0, draggedImage);
        this.updateImageOrders();
      }
    },

    dragEnd() {
      this.draggedIndex = null;
    },

    async updateImageOrders() {
      try {
        // Update order for all images
        for (let i = 0; i < this.images.length; i++) {
          await articleService.updateImage(
            this.articleId,
            this.images[i].id,
            { order: i }
          );
        }
      } catch (error) {
        console.error('خطا در به‌روزرسانی ترتیب تصاویر:', error);
      }
    }
  }
}
</script>

<style scoped>
.article-image-manager {
  background: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
}

.image-manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 2px solid #ddd;
  padding-bottom: 15px;
}

.image-manager-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.btn-add-image {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.btn-add-image:hover {
  background: #45a049;
}

.upload-form {
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #333;
  font-weight: 500;
  font-size: 14px;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
}

.btn-submit {
  width: 100%;
  background: #4CAF50;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-submit:hover:not(:disabled) {
  background: #45a049;
}

.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.images-list {
  display: grid;
  gap: 15px;
}

.image-card {
  display: flex;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
  cursor: move;
  transition: all 0.3s;
  user-select: none;
}

.image-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-color: #4CAF50;
}

.image-preview {
  position: relative;
  width: 150px;
  min-width: 150px;
  height: 150px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.drag-indicator {
  position: absolute;
  top: 5px;
  right: 5px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 3px 6px;
  border-radius: 3px;
  font-size: 12px;
}

.image-info {
  flex: 1;
  padding: 15px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.image-captions {
  margin-bottom: 10px;
}

.image-captions p {
  margin: 5px 0;
  color: #666;
  font-size: 13px;
  line-height: 1.4;
}

.image-actions {
  display: flex;
  gap: 8px;
}

.btn-delete,
.btn-edit {
  flex: 1;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s;
}

.btn-delete {
  background: #f44336;
  color: white;
}

.btn-delete:hover {
  background: #da190b;
}

.btn-edit {
  background: #2196F3;
  color: white;
}

.btn-edit:hover {
  background: #0b7dda;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

/* Modal Styles */
.edit-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ddd;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #333;
}

.modal-content .form-group {
  padding: 0 20px;
  margin-bottom: 15px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #ddd;
  background: #f9f9f9;
}

.btn-save,
.btn-cancel {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-save {
  background: #4CAF50;
  color: white;
}

.btn-save:hover {
  background: #45a049;
}

.btn-cancel {
  background: #f0f0f0;
  color: #333;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

@media (max-width: 768px) {
  .image-card {
    flex-direction: column;
  }

  .image-preview {
    width: 100%;
    height: 200px;
  }

  .modal-content {
    width: 95%;
  }
}
</style>
