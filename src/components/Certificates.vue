<template>
  <section class="certificates">
    <h2 class="section-title animate-on-scroll">گواهی‌نامه‌ها</h2>
    <div class="cert-grid">
      <div class="cert-item animate-on-scroll" v-for="cert in certificates" :key="cert.id">
        <img 
          :src="cert.image_url || 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 200 300%27%3E%3Crect fill=%27%23f5f5f5%27 width=%27200%27 height=%27300%27/%3E%3C/svg%3E'" 
          :alt="cert.title_fa || cert.title_en"
        >
        <p>{{ cert.title_fa || cert.title_en }}</p>
        <p v-if="cert.description_fa || cert.description_en" class="cert-description">{{ cert.description_fa || cert.description_en }}</p>
      </div>
    </div>
  </section>
</template>

<script>
import { certificateService } from '../services/api';

export default {
  name: 'Certificates',
  data() {
    return {
      certificates: [],
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchCertificates();
    this.$nextTick(() => {
      setTimeout(() => {
        const elements = this.$el.querySelectorAll('.animate-on-scroll');
        elements.forEach(el => el.classList.add('in-view'));
      }, 50);
    });
  },
  methods: {
    async fetchCertificates() {
      this.loading = true;
      this.error = null;
      try {
        const response = await certificateService.getAll();
        this.certificates = response.data;
      } catch (err) {
        this.error = 'خطا در بارگذاری گواهی‌نامه‌ها';
        console.error('Error fetching certificates:', err);
        this.certificates = [];
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.certificates {
  padding: 60px 50px;
  background: #f9f9f9;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.certificates > .cert-grid {
  max-width: 1200px;
  width: 100%;
}

.cert-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  margin-top: 50px;
  width: 100%;
}

.cert-item {
  background: #f9f9f9;
  padding: 20px;
  text-align: center;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cert-item:hover {
  transform: translateY(-8px);
}

.cert-item img {
  width: 100%;
  height: 350px;
  object-fit: contain;
  margin-bottom: 20px;
  transition: transform 0.3s ease-out;
}

.cert-item:hover img {
  transform: scale(1.05);
}

.cert-item p {
  font-size: 14px;
  color: #2a2929;
}

.cert-description {
  font-size: 12px !important;
  color: #999 !important;
  margin-top: 8px;
}

@media (max-width: 1024px) {
  .cert-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .certificates {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .cert-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 30px;
  }

  .certificates {
    padding: 30px 20px;
  }

  .cert-item {
    padding: 15px;
  }

  .cert-item img {
    height: 250px;
  }

  .cert-item p {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .certificates {
    padding: 20px 15px;
  }

  .cert-grid {
    gap: 15px;
    margin-top: 20px;
  }

  .cert-item {
    padding: 12px;
  }

  .cert-item img {
    height: 200px;
    margin-bottom: 12px;
  }
}
</style>
