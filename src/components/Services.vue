<template>
  <section id="services" class="services-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">خدمات ما</h2>
        <p class="section-subtitle">راهکارهای حرفه‌ای برای رشد کسب و کار شما</p>
      </div>
      
      <div class="services-grid">
        <div 
          v-for="service in services" 
          :key="service.id"
          class="service-card"
          @click="openService(service)"
        >
          <ImageSlider
            :image="service.image"
            :images="service.images"
            :icon="service.icon"
            :gradient="service.gradient"
            class="service-image"
          />
          <div class="service-content">
            <h3 class="service-title">{{ service.title }}</h3>
            <p class="service-description">{{ service.description }}</p>
            <div class="service-footer">
              <span class="service-price" v-if="service.price">{{ service.price }}</span>
              <button class="service-btn">اطلاعات بیشتر</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Service Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedService" class="service-modal-overlay" @click="closeService">
          <div class="service-modal-content" @click.stop>
            <button class="modal-close" @click="closeService">✕</button>
            
            <ImageSlider
              :image="selectedService.image"
              :images="selectedService.images"
              :icon="selectedService.icon"
              :gradient="selectedService.gradient"
              class="service-modal-image"
            />
            
            <div class="service-modal-body">
              <h2 class="service-modal-title">{{ selectedService.title }}</h2>
              <p class="service-modal-description">{{ selectedService.description }}</p>
              
              <div v-if="selectedService.features && selectedService.features.length > 0" class="service-features">
                <h3 class="features-title">ویژگی‌ها:</h3>
                <ul class="features-list">
                  <li v-for="(feature, index) in selectedService.features" :key="index">
                    <span class="feature-icon">✓</span>
                    {{ feature }}
                  </li>
                </ul>
              </div>
              
              <div class="service-modal-footer">
                <div class="price-box" v-if="selectedService.price">
                  <span class="price-label">قیمت:</span>
                  <span class="price-value">{{ selectedService.price }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSlider } from '../api/services'
import apiClient from '../api/client'
import ImageSlider from './ImageSlider.vue'

const services = ref([])
const selectedService = ref(null)
const loading = ref(true)

const enrichServiceWithSlider = async (service) => {
  let images = []
  
  // Try to get slider images if slider_id is available
  if (service.slider_id) {
    try {
      const response = await getSlider(service.slider_id)
      const sliderData = response?.data || response
      if (sliderData?.images && Array.isArray(sliderData.images) && sliderData.images.length > 0) {
        images = sliderData.images
      }
    } catch (error) {
      console.warn(`Failed to fetch slider ${service.slider_id}:`, error)
    }
  }
  
  // If no images from slider, use the image field
  if (images.length === 0 && service.image) {
    images = [service.image]
  }
  
  console.log(`Service "${service.title}" - Images:`, images)
  
  return {
    ...service,
    images
  }
}

const fetchServices = async () => {
  try {
    loading.value = true
    const response = await apiClient.get('/api/services')
    const data = response.data
    const servicesList = data.data || []
    
    // Enrich services with slider images
    const enrichedServices = await Promise.all(
      servicesList.map(service => enrichServiceWithSlider(service))
    )
    
    services.value = enrichedServices
  } catch (error) {
    console.error('خطا در دریافت خدمات:', error)
    services.value = []
  } finally {
    loading.value = false
  }
}

const openService = async (service) => {
  selectedService.value = service
}

const closeService = () => {
  selectedService.value = null
}

onMounted(() => {
  fetchServices()
})
</script>

<style scoped>
.services-section {
  padding: 6rem 2rem;
  background: #ffffff;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #1a1a1a;
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #666;
  margin-top: 1.5rem;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.service-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.service-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
  border-color: rgba(102, 126, 234, 0.2);
}

.service-image {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px 20px 0 0;
  overflow: hidden;
}

.service-content {
  padding: 1.75rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.service-title {
  font-size: 1.375rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #1a1a1a;
  line-height: 1.3;
}

.service-description {
  font-size: 0.9375rem;
  line-height: 1.6;
  color: #666;
  margin-bottom: 1.25rem;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.service-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
}

.service-price {
  font-size: 1rem;
  font-weight: 700;
  color: #667eea;
}

.service-btn {
  padding: 0.625rem 1.25rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.service-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

/* Modal Styles */
.service-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 2rem;
}

.service-modal-content {
  background: white;
  border-radius: 24px;
  width: 95%;
  max-width: 900px;
  max-height: 95vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-close {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  color: white;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: rgba(0, 0, 0, 0.7);
  transform: rotate(90deg);
}

.service-modal-image {
  height: 60vh;
  max-height: 700px;
  min-height: 400px;
  width: 100%;
  flex-shrink: 0;
  border-radius: 24px 24px 0 0;
}

.service-modal-body {
  padding: 2.5rem;
}

.service-modal-title {
  font-size: 1.875rem;
  font-weight: 800;
  margin-bottom: 1.25rem;
  color: #1a1a1a;
}

.service-modal-description {
  font-size: 1.125rem;
  line-height: 1.8;
  color: #666;
  margin-bottom: 2rem;
}

.service-features {
  margin-bottom: 2rem;
}

.features-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.features-list {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 0.75rem;
}

.features-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background: #f8f9ff;
  border-radius: 10px;
  font-size: 0.9375rem;
  color: #333;
  line-height: 1.5;
}

.feature-icon {
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.75rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.service-modal-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #f0f0f0;
}

.price-box {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.price-label {
  font-size: 0.875rem;
  color: #999;
  font-weight: 600;
}

.price-value {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.contact-btn {
  padding: 1rem 2.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.125rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.contact-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

/* Dark Mode */
.dark-mode .services-section {
  background: #1a1a1a;
}

.dark-mode .section-title {
  color: #ffffff;
}

.dark-mode .section-subtitle {
  color: #a0a0a0;
}

.dark-mode .service-card {
  background: #2d2d2d;
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .service-card:hover {
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.25);
  border-color: rgba(102, 126, 234, 0.3);
}

.dark-mode .service-title {
  color: #ffffff;
}

.dark-mode .service-description {
  color: #a0a0a0;
}

.dark-mode .service-footer {
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .service-modal-content {
  background: #2d2d2d;
}

.dark-mode .service-modal-title {
  color: #ffffff;
}

.dark-mode .service-modal-description {
  color: #a0a0a0;
}

.dark-mode .features-title {
  color: #ffffff;
}

.dark-mode .features-list li {
  background: rgba(255, 255, 255, 0.05);
  color: #e0e0e0;
}

.dark-mode .price-label {
  color: #999;
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .service-modal-content,
.modal-leave-to .service-modal-content {
  transform: scale(0.9);
}

@media (max-width: 768px) {
  .services-section {
    padding: 4rem 1.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .section-subtitle {
    font-size: 1rem;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .service-image {
    height: 180px;
  }
  
  .service-content {
    padding: 1.5rem;
  }
  
  .service-title {
    font-size: 1.25rem;
  }
  
  .service-description {
    font-size: 0.875rem;
  }
  
  .service-modal-body {
    padding: 1.75rem;
  }
  
  .service-modal-title {
    font-size: 1.5rem;
  }
  
  .service-modal-description {
    font-size: 1rem;
  }
  
  .service-modal-footer {
    flex-direction: column;
    align-items: stretch;
  }
  
  .contact-btn {
    width: 100%;
  }
  
  .service-modal-image {
    height: 40vh;
    min-height: 250px;
    max-height: 400px;
  }
  
  .features-list li {
    font-size: 0.875rem;
    padding: 0.75rem;
  }
}
</style>
