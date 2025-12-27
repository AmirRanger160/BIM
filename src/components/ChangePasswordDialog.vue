<template>
  <div v-if="isOpen" class="dialog-overlay" @click.self="close">
    <div class="dialog-content">
      <div class="dialog-header">
        <h2>تغییر رمز عبور</h2>
        <button type="button" class="btn-close" @click="close">×</button>
      </div>

      <form @submit.prevent="submitForm" class="dialog-body">
        <div class="form-group">
          <label for="old-password">رمز عبور فعلی</label>
          <input
            id="old-password"
            v-model="formData.old_password"
            type="password"
            placeholder="رمز عبور فعلی"
            required
          >
          <span v-if="errors.old_password" class="error-message">
            {{ errors.old_password }}
          </span>
        </div>

        <div class="form-group">
          <label for="new-password">رمز عبور جدید</label>
          <input
            id="new-password"
            v-model="formData.new_password"
            type="password"
            placeholder="رمز عبور جدید (حداقل 8 کاراکتر)"
            required
            minlength="8"
          >
          <span v-if="errors.new_password" class="error-message">
            {{ errors.new_password }}
          </span>
          <span v-if="formData.new_password && formData.new_password.length < 8" class="hint-message">
            رمز عبور باید حداقل 8 کاراکتر باشد
          </span>
        </div>

        <div class="form-group">
          <label for="confirm-password">تأیید رمز عبور جدید</label>
          <input
            id="confirm-password"
            v-model="formData.confirm_password"
            type="password"
            placeholder="تأیید رمز عبور جدید"
            required
          >
          <span v-if="errors.confirm_password" class="error-message">
            {{ errors.confirm_password }}
          </span>
        </div>

        <div v-if="errors.general" class="error-alert">
          {{ errors.general }}
        </div>

        <div class="dialog-actions">
          <button type="submit" class="btn-save" :disabled="loading">
            {{ loading ? 'در حال تغییر...' : 'تغییر رمز عبور' }}
          </button>
          <button type="button" class="btn-cancel" @click="close" :disabled="loading">
            لغو
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { adminUserService } from '../services/api'

export default {
  name: 'ChangePasswordDialog',
  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    userId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      formData: {
        old_password: '',
        new_password: '',
        confirm_password: ''
      },
      errors: {},
      loading: false
    }
  },
  methods: {
    validateForm() {
      this.errors = {};

      if (!this.formData.old_password) {
        this.errors.old_password = 'رمز عبور فعلی الزامی است';
      }

      if (!this.formData.new_password) {
        this.errors.new_password = 'رمز عبور جدید الزامی است';
      } else if (this.formData.new_password.length < 8) {
        this.errors.new_password = 'رمز عبور باید حداقل 8 کاراکتر باشد';
      }

      if (!this.formData.confirm_password) {
        this.errors.confirm_password = 'تأیید رمز عبور الزامی است';
      } else if (this.formData.new_password !== this.formData.confirm_password) {
        this.errors.confirm_password = 'رمزهای عبور منطبق نیستند';
      }

      return Object.keys(this.errors).length === 0;
    },
    async submitForm() {
      if (!this.validateForm()) {
        return;
      }

      this.loading = true;
      try {
        await adminUserService.changePassword(this.userId, {
          old_password: this.formData.old_password,
          new_password: this.formData.new_password
        });

        this.$emit('success');
        this.close();
      } catch (error) {
        console.error('Error changing password:', error);
        const detail = error.response?.data?.detail;
        if (detail) {
          this.errors.general = detail;
        } else {
          this.errors.general = 'خطا در تغییر رمز عبور. لطفا دوباره تلاش کنید.';
        }
      } finally {
        this.loading = false;
      }
    },
    close() {
      this.resetForm();
      this.$emit('close');
    },
    resetForm() {
      this.formData = {
        old_password: '',
        new_password: '',
        confirm_password: ''
      };
      this.errors = {};
    }
  }
}
</script>

<style scoped>
.dialog-overlay {
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

.dialog-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 90%;
  animation: slideIn 0.3s ease;
  direction: rtl;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.dialog-header h2 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s ease;
}

.btn-close:hover {
  color: #333;
}

.dialog-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  font-size: 14px;
}

.form-group input {
  padding: 10px 12px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #0099FF;
}

.error-message {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 5px;
}

.hint-message {
  color: #95a5a6;
  font-size: 12px;
  margin-top: 5px;
}

.error-alert {
  background: #fadbd8;
  border: 1px solid #e74c3c;
  color: #c0392b;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 14px;
}

.dialog-actions {
  display: flex;
  gap: 15px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn-save,
.btn-cancel {
  flex: 1;
  padding: 10px 16px;
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

.btn-cancel:hover:not(:disabled) {
  background: #7f8c8d;
}

.btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
