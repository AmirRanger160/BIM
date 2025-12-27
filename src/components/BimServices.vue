<template>
  <section class="bim-services" id="bim">
    <h2 class="section-title animate-on-scroll">خدمات BIM</h2>
    <Loader v-if="loading" />
    <div class="services-grid" v-if="!loading && !error">
      <div class="service-card animate-on-scroll" v-for="service in bimServices" :key="service.id">
        <img 
          :src="service.image_url || 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 300 250%27%3E%3Crect fill=%27%23ddd%27 width=%27300%27 height=%27250%27/%3E%3C/svg%3E'" 
          :alt="service.title_fa || service.title_en || service.title"
        >
        <h3>{{ service.title_fa || service.title_en || service.title }}</h3>
        <p>{{ service.description_fa || service.description_en || service.description }}</p>
        <p v-if="service.software_tools" style="margin-top: 15px;">نرم‌افزارهای مجاز مورد استفاده:</p>
        <div v-if="service.software_tools" class="software-logos">
          <span v-for="(tool, idx) in service.software_tools.split(',').map(t => t.trim())" :key="idx" class="software-tag">{{ tool }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { serviceService } from '../services/api';
import Loader from './Loader.vue';

export default {
  name: 'BimServices',
  components: {
    Loader
  },
  data() {
    return {
      bimServices: [],
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
        const response = await serviceService.getAll({ category: 'BIM' });
        this.bimServices = response.data;
      } catch (err) {
        this.error = 'خطا در بارگذاری خدمات';
        console.error('Error fetching BIM services:', err);
        this.bimServices = [];
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.bim-services {
  padding: 20px 20px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bim-services > .services-grid {
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

.software-logos {
  display: flex;
  justify-content: flex-end;
  gap: 5px;
  flex-wrap: wrap;
}

.software-logos img {
  height: 40px;
  object-fit: contain;
  transition: transform 0.3s ease-out;
}

.software-logos img:hover {
  transform: scale(1.1);
}

.software-tag {
  display: inline-block;
  background: #f0f0f0;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}

@media (max-width: 1024px) {
  .services-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .bim-services {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .services-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 30px;
  }

  .bim-services {
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
  }

  .software-logos {
    gap: 10px;
  }

  .software-logos img {
    height: 30px;
  }
}

@media (max-width: 480px) {
  .bim-services {
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

  .software-logos img {
    height: 25px;
  }
}
</style>
