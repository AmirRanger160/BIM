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
          <span style="white-space: pre-wrap;">{{ errorMessage }}</span>
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
      <iframe
        class="contact-map"
        src="https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d3235.689511977643!2d51.408716999999996!3d35.807555!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m2!1m1!2zMzXCsDQ4JzI3LjIiTiA1McKwMjQnMzEuNCJF!5e0!3m2!1sfa!2s!4v1766832059185!5m2!1sfa!2s"
        width="100%"
        height="400"
        style="border:0;"
        allowfullscreen=""
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade">
      </iframe>
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
      isLoading: false,
      showSuccess: false,
      errorMessage: ''
    }
  },
  mounted() {
    // No need to load company info anymore
  },
  methods: {
    async submitForm() {
      this.errorMessage = '';
      
      // Front-end validation
      const errors = [];
      
      if (!this.form.name || this.form.name.trim() === '') {
        errors.push('نام: لطفا نام خود را وارد کنید');
      } else if (this.form.name.length > 255) {
        errors.push('نام: نام نباید بیشتر از 255 کاراکتر باشد');
      }
      
      if (!this.form.phone || this.form.phone.trim() === '') {
        errors.push('شماره تلفن: لطفا شماره تلفن خود را وارد کنید');
      } else if (this.form.phone.length < 5) {
        errors.push('شماره تلفن: شماره تلفن باید حداقل 5 کاراکتر باشد');
      } else if (this.form.phone.length > 20) {
        errors.push('شماره تلفن: شماره تلفن نباید بیشتر از 20 کاراکتر باشد');
      }
      
      if (!this.form.email || this.form.email.trim() === '') {
        errors.push('ایمیل: لطفا ایمیل خود را وارد کنید');
      } else if (!this.isValidEmail(this.form.email)) {
        errors.push('ایمیل: لطفا ایمیل معتبری وارد کنید');
      }
      
      if (!this.form.message || this.form.message.trim() === '') {
        errors.push('پیام: لطفا پیام خود را وارد کنید');
      } else if (this.form.message.length < 10) {
        errors.push('پیام: پیام باید حداقل 10 کاراکتر باشد');
      }
      
      if (errors.length > 0) {
        this.errorMessage = errors.join('\n');
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
        
        // Handle validation errors from API
        if (error.response?.status === 422 && error.response?.data?.detail) {
          const validationErrors = error.response.data.detail;
          if (Array.isArray(validationErrors)) {
            const messages = validationErrors.map(err => {
              const field = err.loc?.[1] || 'نامعلوم';
              const msg = err.msg || 'خطای تایید';
              
              // Translate field names
              const fieldNames = {
                'name': 'نام',
                'phone': 'شماره تلفن',
                'email': 'ایمیل',
                'message': 'پیام'
              };
              
              return `${fieldNames[field] || field}: ${msg}`;
            });
            this.errorMessage = messages.join('\n');
          } else {
            this.errorMessage = 'خطا در تایید داده‌ها. لطفا مقادیر صحیح وارد کنید.';
          }
        } else {
          this.errorMessage = 'خطا در ارسال پیام. لطفا دوباره تلاش کنید.';
        }
      } finally {
        this.isLoading = false;
      }
    },
    isValidEmail(email) {
      // Basic email validation regex
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
    clearError() {
      this.errorMessage = '';
    }
  }
}
</script>

<style scoped>
.contact {
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
  border-color: #87CEEB;
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
  background: #d4edda;
  padding: 12px 15px;
  border-radius: 6px;
  color: #155724;
}

.error-message {
  display: flex;
  flex-direction: column;
  gap: 5px;
  background: #f8d7da;
  padding: 12px 15px;
  border-radius: 6px;
  color: #721c24;
  font-size: 14px;
  line-height: 1.5;
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
  background: #87CEEB;
  color: white;
  padding: 15px 40px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  font-family: inherit;
  margin-bottom: 100px;
  min-height: 44px;
}

.btn-send:hover:not(:disabled) {
  background: #16a085;
}

.btn-send:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.contact-map {
  width: 100%;
  height: 400px;
}

@media (max-width: 768px) {
  .contact-container {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .contact-map {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .contact-map {
    height: 250px;
  }
}
</style>
