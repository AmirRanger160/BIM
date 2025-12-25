<template>
  <section class="contact" id="contact">
    <h2 class="section-title animate-on-scroll">تماس با ما</h2>
    <div class="contact-container">
      <div class="contact-form animate-on-scroll">
        <div class="form-group">
          <input 
            v-model="form.name" 
            type="text" 
            placeholder="نام شما"
            @keydown="clearError"
          >
        </div>
        <div class="form-group">
          <input 
            v-model="form.phone" 
            type="tel" 
            placeholder="شماره تلفن شما"
            @keydown="clearError"
          >
        </div>
        <div class="form-group">
          <input 
            v-model="form.email" 
            type="email" 
            placeholder="ایمیل شما"
            @keydown="clearError"
          >
        </div>
        <div class="form-group">
          <textarea 
            v-model="form.message" 
            placeholder="پیام شما"
            @keydown="clearError"
          ></textarea>
        </div>
        <div v-if="errorMessage" class="error-message">
          <span>{{ errorMessage }}</span>
        </div>
        <div v-if="showSuccess" class="success-message">
          <div class="success-check">✓</div>
          <span>ارسال شد!</span>
        </div>
        <button 
          class="btn-send"
          @click="submitForm"
          :disabled="isLoading"
        >
          {{ isLoading ? 'در حال ارسال...' : 'ارسال' }}
        </button>
      </div>
      <div class="contact-info animate-on-scroll">
        <div class="company-info">
          <h3>اطلاعات تماس</h3>
          <div v-if="companyInfo" class="info-items">
            <div class="info-item">
              <span class="label">شرکت:</span>
              <span class="value">{{ companyInfo.name }}</span>
            </div>
            <div class="info-item">
              <span class="label">آدرس:</span>
              <span class="value">{{ companyInfo.location }}</span>
            </div>
            <div class="info-item">
              <span class="label">تلفن:</span>
              <span class="value">
                <a :href="`tel:${companyInfo.phone}`">{{ companyInfo.phone }}</a>
              </span>
            </div>
            <div class="info-item">
              <span class="label">ایمیل:</span>
              <span class="value">
                <a :href="`mailto:${companyInfo.email}`">{{ companyInfo.email }}</a>
              </span>
            </div>
            <div v-if="companyInfo.founded_year" class="info-item">
              <span class="label">سال تاسیس:</span>
              <span class="value">{{ companyInfo.founded_year }}</span>
            </div>
          </div>
          <div v-else class="loading">
            <p>در حال بارگذاری...</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { contactService } from '../services/api';

export default {
  name: 'Contact',
  data() {
    return {
      form: {
        name: '',
        phone: '',
        email: '',
        message: ''
      },
      companyInfo: null,
      isLoading: false,
      showSuccess: false,
      errorMessage: ''
    }
  },
  mounted() {
    this.loadCompanyInfo();
  },
  methods: {
    async loadCompanyInfo() {
      try {
        const response = await contactService.getCompanyInfo();
        this.companyInfo = response.data;
      } catch (error) {
        console.error('Error loading company info:', error);
      }
    },
    async submitForm() {
      this.errorMessage = '';
      
      // Validation
      if (!this.form.name || !this.form.phone || !this.form.email || !this.form.message) {
        this.errorMessage = 'لطفا تمام فیلدها را پر کنید';
        return;
      }
      
      this.isLoading = true;
      
      try {
        await contactService.submit({
          name: this.form.name,
          phone: this.form.phone,
          email: this.form.email,
          message: this.form.message
        });
        
        this.showSuccess = true;
        this.form = { name: '', phone: '', email: '', message: '' };
        
        setTimeout(() => {
          this.showSuccess = false;
        }, 5000);
      } catch (error) {
        console.error('Error submitting contact form:', error);
        this.errorMessage = 'خطا در ارسال پیام. لطفا دوباره تلاش کنید.';
      } finally {
        this.isLoading = false;
      }
    },
    clearError() {
      this.errorMessage = '';
    }
  }
}
</script>

<style scoped>
.contact {
  padding: 60px 50px;
  background: #f9f9f9;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.contact > .contact-container {
  max-width: 1200px;
  width: 100%;
}

.contact-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  margin-top: 50px;
  width: 100%;
}

.contact-info {
  border-radius: 8px;
  overflow: hidden;
  background: white;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.company-info h3 {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #1abc9c;
}

.info-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info-item {
  display: flex;
  gap: 15px;
  align-items: flex-start;
}

.info-item .label {
  font-weight: bold;
  color: #333;
  min-width: 80px;
}

.info-item .value {
  color: #666;
}

.info-item a {
  color: #1abc9c;
  text-decoration: none;
  transition: color 0.3s ease;
}

.info-item a:hover {
  color: #16a085;
  text-decoration: underline;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #999;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group input,
.form-group textarea {
  padding: 15px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
  min-height: 50px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #1abc9c;
}

.form-group textarea {
  min-height: 120px;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #999;
}

.success-message {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
  background: #d4edda;
  padding: 12px 15px;
  border-radius: 6px;
  color: #155724;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
  background: #f8d7da;
  padding: 12px 15px;
  border-radius: 6px;
  color: #721c24;
}

.success-check {
  width: 24px;
  height: 24px;
  background: #27ae60;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.btn-send {
  background: #1abc9c;
  color: white;
  padding: 15px 40px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: inherit;
  min-height: 44px;
}

.btn-send:hover:not(:disabled) {
  background: #16a085;
  transform: translateY(-2px);
}

.btn-send:active:not(:disabled) {
  transform: translateY(0);
}

.btn-send:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-send:hover {
  background: #16a085;
  transform: translateY(-2px);
}

.btn-send:active {
  transform: translateY(0);
}

@media (max-width: 1024px) {
  .contact {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .contact {
    padding: 30px 20px;
  }

  .contact-container {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .contact-map img {
    height: 300px;
  }

  .form-group input,
  .form-group textarea {
    padding: 12px;
    font-size: 13px;
    min-height: 44px;
  }

  .btn-send {
    padding: 12px 30px;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .contact {
    padding: 20px 15px;
  }

  .contact-map img {
    height: 250px;
  }

  .form-group input,
  .form-group textarea {
    padding: 10px;
    font-size: 12px;
    min-height: 44px;
  }

  .form-group textarea {
    min-height: 100px;
  }

  .btn-send {
    padding: 10px 25px;
    font-size: 11px;
    min-height: 44px;
  }
}
</style>
