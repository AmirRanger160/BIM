<template>
  <div class="file-upload">
    <div 
      class="upload-area" 
      @click="triggerFileInput" 
      @drop="handleDrop" 
      @dragover.prevent="isDragging = true"
      @dragleave="isDragging = false"
      :class="{ 'drag-over': isDragging }"
    >
      <input
        ref="fileInput"
        type="file"
        :accept="accept"
        @change="handleFileSelect"
        style="display: none"
      >

      <div v-if="!file" class="upload-placeholder">
        <div class="upload-icon">📁</div>
        <p>{{ label || 'فایل را اینجا رها کنید یا کلیک کنید' }}</p>
        <small v-if="accept">فرمت‌های مجاز: {{ accept }}</small>
        <small v-if="maxSize">حداکثر حجم: {{ formatFileSize(maxSize) }}</small>
      </div>

      <div v-else class="file-preview">
        <div class="file-info">
          <span class="file-name">{{ file.name }}</span>
          <span class="file-size">({{ formatFileSize(file.size) }})</span>
        </div>
        <div class="progress-container" v-if="uploadProgress > 0 && uploadProgress < 100">
          <div class="progress-bar" :style="{ width: uploadProgress + '%' }"></div>
          <span class="progress-text">{{ uploadProgress }}%</span>
        </div>
        <button v-else type="button" @click.stop="removeFile" class="btn-remove">×</button>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from '../composables/useToast';

export default {
  name: 'FileUpload',
  props: {
    modelValue: {
      type: [File, String],
      default: null
    },
    accept: {
      type: String,
      default: '*'
    },
    label: {
      type: String,
      default: ''
    },
    maxSize: {
      type: Number,
      default: 10 * 1024 * 1024 // 10MB default
    },
    allowedTypes: {
      type: Array,
      default: null // If null, any type is allowed. Set to ['image/jpeg', 'image/png', etc] to restrict
    }
  },
  data() {
    return {
      file: null,
      error: '',
      isDragging: false,
      uploadProgress: 0
    }
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  watch: {
    modelValue: {
      handler(newVal) {
        if (newVal instanceof File) {
          this.file = newVal;
          this.error = '';
        } else if (typeof newVal === 'string') {
          this.file = null;
          this.error = '';
        } else {
          this.file = null;
          this.error = '';
        }
      },
      immediate: true
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.validateAndSetFile(file);
      }
    },
    handleDrop(event) {
      event.preventDefault();
      this.isDragging = false;
      const file = event.dataTransfer.files[0];
      if (file) {
        this.validateAndSetFile(file);
      }
    },
    validateAndSetFile(file) {
      this.error = '';
      
      // Check file size
      if (file.size > this.maxSize) {
        this.error = `فایل بیش از حد بزرگ است. حداکثر حجم: ${this.formatFileSize(this.maxSize)}`;
        this.toast.error(this.error);
        this.$refs.fileInput.value = '';
        return;
      }

      // Check file type
      if (this.allowedTypes && this.allowedTypes.length > 0) {
        if (!this.allowedTypes.includes(file.type)) {
          this.error = `نوع فایل پشتیبانی نشده است. فرمت‌های مجاز: ${this.allowedTypes.join(', ')}`;
          this.toast.error(this.error);
          this.$refs.fileInput.value = '';
          return;
        }
      }

      this.setFile(file);
    },
    setFile(file) {
      this.file = file;
      this.error = '';
      this.$emit('update:modelValue', file);
      this.$emit('selected', file);
    },
    removeFile() {
      this.file = null;
      this.error = '';
      this.uploadProgress = 0;
      this.$emit('update:modelValue', null);
      this.$refs.fileInput.value = '';
    },
    setUploadProgress(progress) {
      this.uploadProgress = progress;
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
  }
}
</script>

<style scoped>
.file-upload {
  width: 100%;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafafa;
}

.upload-area:hover {
  border-color: #1abc9c;
  background: #f0f9f8;
}

.upload-area.drag-over {
  border-color: #1abc9c;
  background: #e8f9f7;
  box-shadow: 0 0 10px rgba(26, 188, 156, 0.2);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.upload-icon {
  font-size: 48px;
  color: #ccc;
}

.upload-placeholder p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.upload-placeholder small {
  color: #999;
  font-size: 12px;
  display: block;
}

.file-preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 10px 15px;
  border-radius: 6px;
  border: 1px solid #ddd;
}

.file-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.file-name {
  font-weight: bold;
  color: #333;
  font-size: 14px;
}

.file-size {
  color: #666;
  font-size: 12px;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 120px;
}

.progress-bar {
  flex: 1;
  height: 4px;
  background: #1abc9c;
  border-radius: 2px;
  animation: pulse 1s ease-in-out;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.progress-text {
  font-size: 12px;
  color: #666;
  min-width: 30px;
  text-align: right;
}

.btn-remove {
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
}

.btn-remove:hover {
  background: #c0392b;
}

.error-message {
  color: #dc3545;
  font-size: 12px;
  margin-top: 8px;
  padding: 8px;
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  display: block;
}

@media (max-width: 480px) {
  .upload-area {
    padding: 15px;
  }

  .upload-icon {
    font-size: 36px;
  }

  .file-preview {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .btn-remove {
    align-self: flex-end;
  }
}
</style>