<template>
  <section class="surveying-services" id="surveying">
    <h2 class="section-title animate-on-scroll">خدمات نقشه‌برداری</h2>
    <Loader v-if="loading" />
    <div class="services-grid" v-if="!loading && !error">
      <div class="service-card animate-on-scroll" v-for="service in surveyingServices" :key="service.id">
        <img 
          :src="service.image_url || 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 250%27%3E%3Crect fill=%27%23ddd%27 width=%27300%27 height=%27250%27/%3E%3C/svg%3E'" 
          :alt="service.title_fa || service.title_en || service.title"
        >
        <h3>{{ service.title_fa || service.title_en || service.title }}</h3>
        <p>{{ service.description_fa || service.description_en || service.description }}</p>
      </div>
    </div>
  </section>
</template>

<script>
import { serviceService } from '../services/api';
import Loader from './Loader.vue';

export default {
  name: 'SurveyingServices',
  components: {
    Loader
  },
  data() {
    return {
      surveyingServices: [],
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchServices();
    this.$nextTick(() => {
      setTimeout(() => {
        const elements = this.$el.querySelectorAll('.animate-on-scroll');
        elements.forEach(el => el.classList.add('in-view'));
      }, 50);
    });
  },
  methods: {
    async fetchServices() {
      this.loading = true;
      this.error = null;
      try {
        const response = await serviceService.getAll({ category: 'Surveying' });
        this.surveyingServices = response.data;
      } catch (err) {
        this.error = 'خطا در بارگذاری خدمات';
        console.error('Error fetching surveying services:', err);
        this.surveyingServices = [];
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.surveying-services {
  padding: 20px 20px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.surveying-services > .services-grid {
  max-width: 1200px;
  width: 100%;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 70px;
  width: 100%;
  margin-top: 50px;
}

.service-card {
  background: #ffffff;
  text-align: right;
  cursor: pointer;
}

.service-card img {
  width: 100%;
  height: 250px;
  object-fit: cover;
  margin-bottom: 20px;
}

.service-card h3 {
  font-size: 19px;
  font-weight: bold;
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word;
  text-align: right;
  padding: 15px 0;
}

.service-card p {
  font-size: 14px;
  line-height: 1.8;
  color: #2a2929;
  margin-bottom: 25px;
}

@media (max-width: 1024px) {
  .services-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .surveying-services {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .services-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 30px;
  }

  .surveying-services {
    padding: 30px 20px;
  }

  .service-card {
    padding: 20px;
  }

  .service-card img {
    height: 200px;
    margin-bottom: 15px;
  }

  .service-card h3 {
    font-size: 16px;
    margin-bottom: 10px;
    padding: 12px 0;
  }

  .service-card p {
    font-size: 12px;
    margin-bottom: 15px;
    line-height: 1.6;
  }
}

@media (max-width: 480px) {
  .surveying-services {
    padding: 20px 15px;
  }

  .services-grid {
    gap: 15px;
    margin-top: 20px;
  }

  .service-card {
    padding: 15px;
  }

  .service-card img {
    height: 180px;
    margin-bottom: 15px;
  }

  .service-card h3 {
    font-size: 13px;
    margin-bottom: 8px;
    padding: 10px 0;
  }

  .service-card p {
    font-size: 11px;
    margin-bottom: 12px;
    line-height: 1.6;
  }
}
</style>
