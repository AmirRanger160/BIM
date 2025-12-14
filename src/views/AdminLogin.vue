<template>
  <div class="admin-login">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>🔐 ورود به پنل مدیریت</h1>
          <p>لطفا اطلاعات خود را وارد کنید</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="email">ایمیل</label>
            <input
              id="email"
              v-model="credentials.email"
              type="email"
              placeholder="admin@example.com"
              required
            />
          </div>

          <div class="form-group">
            <label for="password">رمز عبور</label>
            <input
              id="password"
              v-model="credentials.password"
              type="password"
              placeholder="رمز عبور خود را وارد کنید"
              required
            />
          </div>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <button type="submit" class="login-button" :disabled="loading">
            <span v-if="loading">در حال ورود...</span>
            <span v-else>ورود به پنل</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { adminService } from '../api/services'

const router = useRouter()
const credentials = ref({
  email: '',
  password: ''
})
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await adminService.login(credentials.value)
    
    // ذخیره توکن
    localStorage.setItem('admin_token', response.access_token)
    localStorage.setItem('admin_user', JSON.stringify(response.user || {}))
    
    // هدایت به داشبورد
    router.push('/admin/dashboard')
  } catch (err) {
    error.value = err.response?.data?.detail || 'خطا در ورود. لطفا دوباره تلاش کنید.'
  } finally {
    loading.value = false
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
  padding: 2rem;
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background: white;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #2d3748;
}

.login-header p {
  color: #718096;
  font-size: 0.95rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #2d3748;
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.875rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s;
  font-family: inherit;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.875rem;
  border-radius: 10px;
  font-size: 0.9rem;
  text-align: center;
  border: 1px solid #fcc;
}

.login-button {
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 0.5rem;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .login-card {
    padding: 2rem;
  }
  
  .login-header h1 {
    font-size: 1.5rem;
  }
}
</style>
