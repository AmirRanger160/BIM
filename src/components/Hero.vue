<template>
  <section id="home" class="hero">
    <div class="hero-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>
    
    <div class="container">
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-dot"></span>
          اولین در ایران
        </div>
        
        <h1 class="hero-title">
          مهندسین مشاور
          <span class="gradient-text">دانش بنیان بیم</span>
          پیشرو در صنعت
        </h1>
        
        <p class="hero-subtitle">
          ارائه خدمات مهندسی، مشاوره و نظارت در پروژه‌های عمرانی
          <br />
          با بهره‌گیری از جدیدترین تکنولوژی‌های روز دنیا
        </p>
        
        <div class="hero-buttons">
          <button class="btn btn-primary">
            شروع کنید
            <span class="btn-arrow">←</span>
          </button>
          <button 
            v-if="featuredVideo"
            @click="openVideoModal"
            class="btn btn-secondary"
          >
            <span class="play-icon">▶</span>
            تماشای ویدیو
          </button>
        </div>
        
        <div class="hero-stats">
          <div class="stat">
            <div class="stat-value">۱۰۰+</div>
            <div class="stat-label">پروژه موفق</div>
          </div>
          <div class="stat">
            <div class="stat-value">۵۰+</div>
            <div class="stat-label">مشتری راضی</div>
          </div>
          <div class="stat">
            <div class="stat-value">۲۴/۷</div>
            <div class="stat-label">پشتیبانی</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Video Modal -->
  <VideoModal 
    :is-open="showVideoModal" 
    :video="featuredVideo"
    @close="showVideoModal = false"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import VideoModal from './VideoModal.vue'

const showVideoModal = ref(false)
const featuredVideo = ref(null)

onMounted(async () => {
  // بارگذاری ویدیوی اول (اولویت دار)
  try {
    const response = await fetch('/api/videos?active_only=true&limit=1')
    if (response.ok) {
      const videos = await response.json()
      if (videos.length > 0) {
        featuredVideo.value = videos[0]
      }
    }
  } catch (error) {
    console.error('خطا در بارگذاری ویدیو:', error)
  }
})

const openVideoModal = () => {
  showVideoModal.value = true
}
</script>

<style scoped>
.hero {
  position: relative;
  padding: 8rem 0 6rem;
  overflow: hidden;
  min-height: 90vh;
  display: flex;
  align-items: center;
}

.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  top: -200px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  bottom: -150px;
  left: -100px;
  animation-delay: 5s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 1;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #667eea;
  margin-bottom: 2rem;
  animation: fadeInDown 0.8s ease;
}

.badge-dot {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.2);
  }
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  color: #1a1a1a;
  animation: fadeInUp 0.8s ease 0.2s both;
}

.dark-mode .hero-title {
  color: #ffffff;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.8;
  color: #6c757d;
  margin-bottom: 3rem;
  animation: fadeInUp 0.8s ease 0.4s both;
}

.dark-mode .hero-subtitle {
  color: #a0a0a0;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 4rem;
  animation: fadeInUp 0.8s ease 0.6s both;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
}

.btn-primary .btn-arrow {
  transition: transform 0.3s ease;
}

.btn-primary:hover .btn-arrow {
  transform: translateX(-5px);
}

.btn-secondary {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 2px solid rgba(102, 126, 234, 0.3);
}

.dark-mode .btn-secondary {
  color: #a0a0ff;
  background: rgba(102, 126, 234, 0.15);
}

.btn-secondary:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateY(-3px);
}

.play-icon {
  font-size: 0.8rem;
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 3rem;
  max-width: 600px;
  margin: 0 auto;
  animation: fadeInUp 0.8s ease 0.8s both;
}

.stat {
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.dark-mode .stat-label {
  color: #a0a0a0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 4rem 0 3rem;
    min-height: auto;
  }
  
  .container {
    padding: 0 1.5rem;
  }
  
  .hero-badge {
    font-size: 0.85rem;
    padding: 0.4rem 1.2rem;
    margin-bottom: 1.5rem;
  }
  
  .hero-title {
    font-size: 2.2rem;
    line-height: 1.3;
  }
  
  .hero-subtitle {
    font-size: 1rem;
    margin-bottom: 2rem;
  }
  
  .hero-buttons {
    margin-bottom: 3rem;
  }
  
  .hero-stats {
    gap: 1.5rem;
    grid-template-columns: repeat(3, 1fr);
  }
  
  .stat-value {
    font-size: 1.8rem;
  }
  
  .stat-label {
    font-size: 0.8rem;
  }
  
  .gradient-orb {
    filter: blur(60px);
  }
  
  .orb-1 {
    width: 300px;
    height: 300px;
  }
  
  .orb-2 {
    width: 250px;
    height: 250px;
  }
  
  .orb-3 {
    width: 200px;
    height: 200px;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 3rem 0 2rem;
  }
  
  .hero-title {
    font-size: 1.8rem;
  }
  
  .hero-subtitle {
    font-size: 0.95rem;
    line-height: 1.6;
  }
  
  .btn {
    padding: 0.8rem 1.5rem;
    font-size: 0.95rem;
  }
  
  .hero-stats {
    gap: 1rem;
  }
  
  .stat-value {
    font-size: 1.5rem;
  }
  
  .stat-label {
    font-size: 0.75rem;
  }
}
</style>
