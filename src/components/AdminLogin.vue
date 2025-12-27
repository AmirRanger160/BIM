<template>
  <div class="admin-login">
    <div class="login-container">
      <div class="login-card">
        <!-- Logo -->
        <div class="logo-section">
          <img src="/logo b1m 404/لوگو-404-مشاور-بیم.png" alt="BIM Logo" class="login-logo" title="لوگو مشاور BIM">
        </div>

        <h2 class="login-title">ورود به پنل مدیریت</h2>
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">نام کاربری</label>
            <input
              id="username"
              v-model="credentials.username"
              type="text"
              placeholder="نام کاربری خود را وارد کنید"
              @input="clearError"
              required
            >
          </div>
          <div class="form-group">
            <label for="password">رمز عبور</label>
            <input
              id="password"
              v-model="credentials.password"
              type="password"
              placeholder="رمز عبور خود را وارد کنید"
              @input="clearError"
              required
            >
          </div>
          <div v-if="errorMessage" class="error-message">
            <span>{{ errorMessage }}</span>
          </div>
          <button
            type="submit"
            class="btn-login"
            :disabled="isLoading"
          >
            {{ isLoading ? 'در حال ورود...' : 'ورود' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAuthService } from '../services/api';

export default {
  name: 'AdminLogin',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      isLoading: false,
      errorMessage: ''
    }
  },
  provide() {
    return {
      navigateTo: this.navigateTo
    }
  },
  inject: ['navigateTo'],
  methods: {
    async handleLogin() {
      this.errorMessage = '';

      if (!this.credentials.username || !this.credentials.password) {
        this.errorMessage = 'لطفا نام کاربری و رمز عبور را وارد کنید';
        return;
      }

      this.isLoading = true;

      try {
        const response = await adminAuthService.login({
          username: this.credentials.username,
          password: this.credentials.password
        });

        // Store token
        localStorage.setItem('admin_token', response.data.access_token);

        // Navigate to dashboard
        this.navigateTo('/admin');
      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = error.response?.data?.detail || 'خطا در ورود. لطفا دوباره تلاش کنید.';
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
.admin-login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 50px 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.logo-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-logo {
  height: 100px;
  width: auto;
  object-fit: contain;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.login-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 30px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: right;
}

.form-group label {
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  font-size: 14px;
}

.form-group input {
  padding: 12px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-family: inherit;
  font-size: 14px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input::placeholder {
  color: #999;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px 15px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
  border: 1px solid #f5c6cb;
}

.btn-login {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 14px 40px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
  transition: all 0.3s ease;
  margin-top: 10px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }

  .logo-section {
    margin-bottom: 20px;
    padding: 15px;
  }

  .login-logo {
    height: 80px;
  }

  .login-title {
    font-size: 20px;
    margin-bottom: 20px;
  }

  .form-group input {
    padding: 11px 12px;
    font-size: 16px;
  }

  .btn-login {
    padding: 12px 30px;
    font-size: 14px;
  }
}
</style>