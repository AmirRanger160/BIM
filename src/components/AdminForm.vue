<template>
  <div class="admin-form">
    <form @submit.prevent="handleSubmit">
      <div class="form-grid">
        <div
          v-for="field in getFields()"
          :key="field.key"
          class="form-group"
          :class="{ 'has-error': errors[field.key] }"
        >
          <label :for="field.key">
            {{ field.label }}
            <span v-if="field.required" class="required">*</span>
          </label>

          <!-- Text Input -->
          <input
            v-if="field.type === 'text'"
            :id="field.key"
            v-model="formData[field.key]"
            :type="field.inputType || 'text'"
            :placeholder="field.placeholder"
            @blur="validateField(field)"
            :disabled="saving"
          >

          <!-- Email Input -->
          <input
            v-else-if="field.type === 'email'"
            :id="field.key"
            v-model="formData[field.key]"
            type="email"
            :placeholder="field.placeholder"
            @blur="validateField(field)"
            :disabled="saving"
          >

          <!-- Number Input -->
          <input
            v-else-if="field.type === 'number'"
            :id="field.key"
            v-model.number="formData[field.key]"
            type="number"
            :placeholder="field.placeholder"
            @blur="validateField(field)"
            :disabled="saving"
          >

          <!-- Textarea -->
          <textarea
            v-else-if="field.type === 'textarea'"
            :id="field.key"
            v-model="formData[field.key]"
            :placeholder="field.placeholder"
            :rows="field.rows || 4"
            @blur="validateField(field)"
            :disabled="saving"
          ></textarea>

          <!-- Rich Text Editor -->
          <RichTextEditor
            v-else-if="field.type === 'richtext'"
            :model-value="formData[field.key] || ''"
            :placeholder="field.placeholder"
            @update:modelValue="(value) => { formData[field.key] = value; validateField(field); }"
          />

          <!-- Select -->
          <select
            v-else-if="field.type === 'select'"
            :id="field.key"
            v-model="formData[field.key]"
            @blur="validateField(field)"
            :disabled="saving"
          >
            <option value="">انتخاب کنید</option>
            <option
              v-for="option in field.options"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>

          <!-- Checkbox -->
          <div v-else-if="field.type === 'checkbox'" class="checkbox-group">
            <input
              :id="field.key"
              v-model="formData[field.key]"
              type="checkbox"
              :disabled="saving"
            >
            <label :for="field.key" class="checkbox-label">{{ field.label }}</label>
          </div>

          <!-- Date Input -->
          <input
            v-else-if="field.type === 'date'"
            :id="field.key"
            v-model="formData[field.key]"
            type="date"
            @blur="validateField(field)"
            :disabled="saving"
          >

          <!-- File Upload -->
          <FileUpload
            v-else-if="field.type === 'file'"
            :id="field.key"
            v-model="formData[field.key]"
            :accept="field.accept"
            :label="field.label"
            :max-size="field.maxSize || 10 * 1024 * 1024"
            :allowed-types="field.allowedTypes"
            @selected="validateField(field)"
          />

          <!-- Error Message -->
          <span v-if="errors[field.key]" class="error-text">
            {{ errors[field.key] }}
          </span>
        </div>
      </div>

      <div class="form-actions">
        <button 
          type="submit" 
          class="btn-save" 
          :disabled="saving || hasErrors"
          @click.prevent="handleSubmit"
        >
          {{ saving ? 'در حال ذخیره...' : 'ذخیره' }}
        </button>
        <button 
          type="button" 
          @click="handleCancel" 
          class="btn-cancel"
          :disabled="saving"
        >
          لغو
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { useFormValidation } from '../composables/useFormValidation';
import { useToast } from '../composables/useToast';
import FileUpload from './FileUpload.vue'
import RichTextEditor from './RichTextEditor.vue'
import { uploadService } from '../services/api';

export default {
  name: 'AdminForm',
  components: {
    FileUpload,
    RichTextEditor
  },
  props: {
    contentType: {
      type: String,
      required: true
    },
    item: {
      type: Object,
      default: null
    }
  },
  setup() {
    const validation = useFormValidation();
    const toast = useToast();
    return { validation, toast };
  },
  data() {
    return {
      formData: {},
      saving: false,
      errors: {},
      touched: {}
    }
  },
  computed: {
    hasErrors() {
      return Object.keys(this.errors).some(key => this.errors[key] !== null && this.errors[key] !== undefined && this.errors[key] !== '');
    }
  },
  mounted() {
    this.initializeForm();
  },
  watch: {
    item: {
      handler() {
        this.initializeForm();
      },
      deep: true
    }
  },
  methods: {
    initializeForm() {
      const fields = this.getFields();
      this.formData = {};
      this.errors = {};
      this.touched = {};

      fields.forEach(field => {
        if (this.item && this.item[field.key] !== undefined) {
          this.formData[field.key] = this.item[field.key];
        } else {
          this.formData[field.key] = field.default || '';
        }
        this.errors[field.key] = null;
        this.touched[field.key] = false;
      });
    },
    getFields() {
      // Define fields based on content type
      switch (this.contentType) {
        case 'articles':
          return [
            { key: 'title_fa', label: 'عنوان (فارسی)', type: 'text', placeholder: 'عنوان مقاله به فارسی', required: true },
            { key: 'title_en', label: 'عنوان (انگلیسی)', type: 'text', placeholder: 'Article title in English', required: true },
            { key: 'slug', label: 'اسلاگ', type: 'text', placeholder: 'article-slug', required: true },
            { key: 'summary_fa', label: 'خلاصه (فارسی)', type: 'textarea', placeholder: 'خلاصه مقاله به فارسی', rows: 3, required: true },
            { key: 'summary_en', label: 'خلاصه (انگلیسی)', type: 'textarea', placeholder: 'Article summary in English', rows: 3, required: true },
            { key: 'content_fa', label: 'محتوا (فارسی)', type: 'richtext', placeholder: 'محتوای مقاله به فارسی', required: true },
            { key: 'content_en', label: 'محتوا (انگلیسی)', type: 'richtext', placeholder: 'Article content in English', required: true },
            { key: 'category', label: 'دسته‌بندی', type: 'text', placeholder: 'دسته‌بندی مقاله' },
            { key: 'tags', label: 'برچسب‌ها', type: 'text', placeholder: 'برچسب1, برچسب2' },
            { key: 'author', label: 'نویسنده', type: 'text', placeholder: 'نام نویسنده' },
            { key: 'image_url', label: 'تصویر شاخص', type: 'file', accept: 'image/*', allowedTypes: ['image/jpeg', 'image/png', 'image/webp'], maxSize: 5 * 1024 * 1024 },
            { key: 'is_published', label: 'منتشر شود', type: 'checkbox' }
          ];
        case 'projects':
          return [
            { key: 'title_fa', label: 'عنوان (فارسی)', type: 'text', placeholder: 'عنوان پروژه به فارسی', required: true },
            { key: 'title_en', label: 'عنوان (انگلیسی)', type: 'text', placeholder: 'Project title in English', required: true },
            { key: 'description_fa', label: 'توضیحات (فارسی)', type: 'textarea', placeholder: 'توضیحات پروژه به فارسی', rows: 4, required: true },
            { key: 'description_en', label: 'توضیحات (انگلیسی)', type: 'textarea', placeholder: 'Project description in English', rows: 4, required: true },
            {
              key: 'category',
              label: 'دسته‌بندی',
              type: 'select',
              options: [
                { value: 'BIM', label: 'BIM' },
                { value: 'Surveying', label: 'Surveying' }
              ],
              required: true
            },
            { key: 'image_url', label: 'تصویر شاخص', type: 'file', accept: 'image/*', allowedTypes: ['image/jpeg', 'image/png', 'image/webp'], maxSize: 5 * 1024 * 1024 },
            { key: 'archive_url', label: 'لینک دانلود آرشیو', type: 'text', placeholder: 'https://...' },
            { key: 'iframe_url', label: 'URL iframe', type: 'text', placeholder: 'https://...' },
            { key: 'order', label: 'ترتیب نمایش', type: 'number', default: 0 },
            { key: 'is_featured', label: 'پروژه برجسته', type: 'checkbox' }
          ];
        case 'services':
          return [
            { key: 'title', label: 'عنوان', type: 'text', placeholder: 'عنوان خدمت', required: true },
            { key: 'description', label: 'توضیحات', type: 'textarea', placeholder: 'توضیحات خدمت', rows: 4, required: true },
            {
              key: 'category',
              label: 'دسته‌بندی',
              type: 'select',
              options: [
                { value: 'BIM', label: 'BIM' },
                { value: 'Surveying', label: 'Surveying' }
              ],
              required: true
            },
            { key: 'image_url', label: 'تصویر شاخص', type: 'file', accept: 'image/*', allowedTypes: ['image/jpeg', 'image/png', 'image/webp'], maxSize: 5 * 1024 * 1024 },
            { key: 'software_tools', label: 'ابزارهای نرم‌افزاری', type: 'text', placeholder: 'ابزار1, ابزار2' }
          ];
        case 'team':
          return [
            { key: 'name_fa', label: 'نام (فارسی)', type: 'text', placeholder: 'نام عضو تیم به فارسی', required: true },
            { key: 'name_en', label: 'نام (انگلیسی)', type: 'text', placeholder: 'Member name in English', required: true },
            { key: 'position_fa', label: 'سمت (فارسی)', type: 'text', placeholder: 'سمت عضو تیم به فارسی', required: true },
            { key: 'position_en', label: 'سمت (انگلیسی)', type: 'text', placeholder: 'Position in English', required: true },
            { key: 'email', label: 'ایمیل', type: 'email', placeholder: 'email@example.com', required: true },
            { key: 'phone', label: 'شماره تلفن', type: 'text', placeholder: '۰۹۱۲۱۲۳۴۵۶۷' },
            { key: 'bio_fa', label: 'بیوگرافی (فارسی)', type: 'textarea', placeholder: 'بیوگرافی عضو تیم به فارسی', rows: 4 },
            { key: 'bio_en', label: 'بیوگرافی (انگلیسی)', type: 'textarea', placeholder: 'Team member bio in English', rows: 4 },
            { key: 'image_url', label: 'تصویر پروفایل', type: 'file', accept: 'image/*', allowedTypes: ['image/jpeg', 'image/png', 'image/webp'], maxSize: 5 * 1024 * 1024 }
          ];
        case 'certificates':
          return [
            { key: 'title_en', label: 'عنوان (انگلیسی)', type: 'text', placeholder: 'Certificate title in English', required: true },
            { key: 'title_fa', label: 'عنوان (فارسی)', type: 'text', placeholder: 'عنوان گواهینامه به فارسی', required: false },
            { key: 'description_fa', label: 'توضیحات (فارسی)', type: 'textarea', placeholder: 'توضیحات گواهینامه به فارسی', rows: 4 },
            { key: 'description_en', label: 'توضیحات (انگلیسی)', type: 'textarea', placeholder: 'Certificate description in English', rows: 4 },
            { key: 'issue_date', label: 'تاریخ صدور', type: 'text', placeholder: '۱۴۰۲/۰۱/۱۵' },
            { key: 'expiry_date', label: 'تاریخ انقضا', type: 'text', placeholder: '۱۴۰۴/۰۱/۱۵' },
            { key: 'image_url', label: 'تصویر گواهینامه', type: 'file', accept: 'image/*', allowedTypes: ['image/jpeg', 'image/png', 'image/webp'], maxSize: 5 * 1024 * 1024 }
          ];
        case 'licenses':
          return [
            { key: 'title_en', label: 'عنوان (انگلیسی)', type: 'text', placeholder: 'License title in English', required: true },
            { key: 'title_fa', label: 'عنوان (فارسی)', type: 'text', placeholder: 'عنوان مجوز به فارسی', required: false },
            { key: 'description_fa', label: 'توضیحات (فارسی)', type: 'textarea', placeholder: 'توضیحات مجوز به فارسی', rows: 4 },
            { key: 'description_en', label: 'توضیحات (انگلیسی)', type: 'textarea', placeholder: 'License description in English', rows: 4 },
            { key: 'issue_date', label: 'تاریخ صدور', type: 'text', placeholder: '۱۴۰۲/۰۱/۱۵' },
            { key: 'issue_authority', label: 'مرجع صادرکننده', type: 'text', placeholder: 'نام مرجع صادرکننده', required: true },
            { key: 'image_url', label: 'تصویر مجوز', type: 'file', accept: 'image/*', allowedTypes: ['image/jpeg', 'image/png', 'image/webp'], maxSize: 5 * 1024 * 1024 }
          ];
        case 'contacts':
          return [
            { key: 'name', label: 'نام', type: 'text', placeholder: 'نام تماس گیرنده', required: true },
            { key: 'email', label: 'ایمیل', type: 'email', placeholder: 'email@example.com', required: true },
            { key: 'phone', label: 'شماره تلفن', type: 'text', placeholder: '۰۹۱۲۱۲۳۴۵۶۷' },
            { key: 'message', label: 'پیام', type: 'textarea', placeholder: 'پیام کاربر', rows: 6, required: true },
            {
              key: 'status',
              label: 'وضعیت',
              type: 'select',
              options: [
                { value: 'new', label: 'جدید' },
                { value: 'read', label: 'خوانده شده' },
                { value: 'replied', label: 'پاسخ داده شده' }
              ]
            }
          ];
        default:
          return [
            { key: 'title_fa', label: 'عنوان (فارسی)', type: 'text', required: true },
            { key: 'title_en', label: 'عنوان (انگلیسی)', type: 'text', required: true },
            { key: 'description_fa', label: 'توضیحات (فارسی)', type: 'textarea', required: true },
            { key: 'description_en', label: 'توضیحات (انگلیسی)', type: 'textarea', required: true }
          ];
      }
    },
    validateField(field) {
      const value = this.formData[field.key];
      let error = null;

      if (field.required) {
        if (!value || (typeof value === 'string' && value.trim() === '')) {
          error = `${field.label} الزامی است`;
        }
      }

      if (!error && field.type === 'email' && value) {
        if (!this.validation.isValidEmail(value)) {
          error = `${field.label} نامعتبر است`;
        }
      }

      if (!error && field.type === 'number' && value !== '' && value !== null) {
        if (isNaN(value)) {
          error = `${field.label} باید عدد باشد`;
        }
      }

      this.errors[field.key] = error;
      this.touched[field.key] = true;
    },
    handleCancel() {
      this.formData = {};
      this.errors = {};
      this.touched = {};
      this.$emit('cancel');
    },
    async uploadFileIfNeeded(file, fieldKey) {
      /**Upload a file and return its URL, or return empty string if no file */
      if (!file || !(file instanceof File)) {
        return '';
      }
      try {
        const response = await uploadService.uploadImage(file);
        return response.data.url || '';
      } catch (error) {
        console.error(`Error uploading ${fieldKey}:`, error);
        this.toast.error(`خطا در آپلود ${fieldKey}`);
        throw error;
      }
    },
    async prepareFormData() {
      // Create a clean copy of form data for submission
      const cleanData = { ...this.formData };
      const fields = this.getFields();

      // Process each field and upload files
      for (const field of fields) {
        const value = cleanData[field.key];

        // Upload file and replace with URL
        if (field.type === 'file' && value instanceof File) {
          cleanData[field.key] = await this.uploadFileIfNeeded(value, field.label);
        }

        // Ensure number fields are actual numbers
        if (field.type === 'number') {
          cleanData[field.key] = value === '' || value === null ? 0 : Number(value);
        }

        // Ensure checkbox fields are booleans
        if (field.type === 'checkbox') {
          cleanData[field.key] = Boolean(value);
        }
      }

      return cleanData;
    },
    async handleSubmit() {
      // Validate all fields before submission
      const fields = this.getFields();
      let hasErrors = false;

      fields.forEach(field => {
        this.validateField(field);
        if (this.errors[field.key]) {
          hasErrors = true;
        }
      });

      if (hasErrors) {
        this.toast.error('لطفا تمام خطاهای فرم را برطرف کنید');
        return;
      }

      this.saving = true;
      try {
        const cleanData = await this.prepareFormData();
        await this.$emit('save', cleanData);
        this.toast.success(this.item ? 'تغییرات ذخیره شد' : 'رکورد جدید افزوده شد');
      } catch (error) {
        console.error('Save error:', error);
        this.toast.error('خطا در ذخیره‌سازی: ' + (error.message || 'خطای نامشخص'));
      } finally {
        this.saving = false;
      }
    }
  }
}
</script>

<style scoped>
.admin-form {
  max-width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.has-error input,
.form-group.has-error textarea,
.form-group.has-error select {
  border-color: #dc3545;
  background-color: #fff5f5;
}

.form-group label {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
  font-size: 14px;
}

.required {
  color: #dc3545;
  margin-left: 4px;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 10px 12px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  transition: all 0.3s ease;
}

.form-group input:hover,
.form-group textarea:hover,
.form-group select:hover {
  border-color: #bbb;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #0099FF;
  box-shadow: 0 0 0 3px rgba(0, 153, 255, 0.1);
}

.form-group input:disabled,
.form-group textarea:disabled,
.form-group select:disabled {
  background-color: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-label {
  font-weight: normal !important;
  margin-bottom: 0 !important;
  cursor: pointer;
}

.error-text {
  color: #dc3545;
  font-size: 12px;
  margin-top: 6px;
  display: block;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn-save,
.btn-cancel {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-save {
  background: #0099FF;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #0077cc;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #95a5a6;
  color: white;
}

.btn-cancel:hover {
  background: #7f8c8d;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-save,
  .btn-cancel {
    width: 100%;
  }
}
</style>