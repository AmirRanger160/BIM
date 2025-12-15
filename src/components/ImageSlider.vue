<template>
  <div class="image-slider" :class="{ 'has-multiple': hasMultipleImages }">
    <!-- تصویر اصلی / اسلایدر -->
    <div v-if="displayImages && displayImages.length > 0" class="slider-container">
      <TransitionGroup name="slide-fade" tag="div" class="slides">
        <div 
          v-for="(img, index) in displayImages" 
          :key="`slide-${currentSlide}-${index}`"
          v-show="index === currentSlide"
          class="slide"
          :style="getSlideStyle(img)"
        >
          <div class="slide-overlay" :style="{ background: gradient }"></div>
          <div v-if="getSlideIcon(img)" class="slide-icon">{{ getSlideIcon(img) }}</div>
        </div>
      </TransitionGroup>

      <!-- نقاط ناوبری -->
      <div v-if="displayImages.length > 1" class="slider-dots">
        <button
          v-for="(img, index) in displayImages"
          :key="`dot-${index}`"
          :class="['dot', { active: index === currentSlide }]"
          @click="goToSlide(index)"
          :aria-label="`اسلاید ${index + 1}`"
        ></button>
      </div>

      <!-- دکمه‌های قبل/بعد -->
      <button 
        v-if="displayImages.length > 1"
        class="slider-arrow prev"
        @click="prevSlide"
        aria-label="اسلاید قبلی"
      >
        ‹
      </button>
      <button 
        v-if="displayImages.length > 1"
        class="slider-arrow next"
        @click="nextSlide"
        aria-label="اسلاید بعدی"
      >
        ›
      </button>
    </div>

    <!-- fallback به تصویر شاخص -->
    <div v-else-if="image" class="image-placeholder" :style="{ backgroundImage: `url(${getImageUrl(image)})` }">
      <div class="slide-overlay" :style="{ background: gradient }"></div>
      <div v-if="icon" class="slide-icon">{{ icon }}</div>
    </div>

    <!-- fallback نهایی: gradient فقط بدون icon -->
    <div v-else class="gradient-placeholder" :style="{ background: gradient }">
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  image: {
    type: String,
    default: null
  },
  images: {
    type: Array,
    default: () => []
  },
  icon: {
    type: String,
    default: null
  },
  gradient: {
    type: String,
    default: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  autoplay: {
    type: Boolean,
    default: true
  },
  interval: {
    type: Number,
    default: 4000 // 4 ثانیه
  },
  apiBaseUrl: {
    type: String,
    default: ''
  }
})

const currentSlide = ref(0)
let autoplayTimer = null

// تنظیم عکس‌های نمایشی
const displayImages = computed(() => {
  // 1. اگر slider موجود بود، images استفاده کن
  if (props.images && props.images.length > 0) {
    return props.images
  }
  // 2. اگر slider نبود اما تصویر شاخص موجود بود، آن را استفاده کن
  if (props.image) {
    return [props.image]
  }
  // 3. اگر هیچ کدام نبود، خالی برگردان
  return []
})

const hasMultipleImages = computed(() => {
  return displayImages.value.length > 1
})

// تبدیل URL نسبی به مطلق
const getImageUrl = (url) => {
  if (!url) return ''
  if (typeof url !== 'string') return ''
  if (url.startsWith('http')) return url
  const baseUrl = props.apiBaseUrl || import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  return `${baseUrl}${url}`
}

// استخراج تصویر URL از object یا string
const getImageFromItem = (item) => {
  if (typeof item === 'string') {
    return item
  }
  if (item && typeof item === 'object') {
    return item.image || ''
  }
  return ''
}

// استخراج icon از object یا fallback
const getSlideIcon = (item) => {
  if (typeof item === 'string') {
    return props.icon || null
  }
  if (item && typeof item === 'object') {
    return item.icon || props.icon || null
  }
  return props.icon || null
}

// دریافت style برای slide
const getSlideStyle = (item) => {
  const imageUrl = getImageFromItem(item)
  if (imageUrl) {
    return { backgroundImage: `url(${getImageUrl(imageUrl)})` }
  }
  return {}
}

const nextSlide = () => {
  if (displayImages.value.length > 0) {
    currentSlide.value = (currentSlide.value + 1) % displayImages.value.length
  }
}

const prevSlide = () => {
  if (displayImages.value.length > 0) {
    currentSlide.value = currentSlide.value === 0 
      ? displayImages.value.length - 1 
      : currentSlide.value - 1
  }
}

const goToSlide = (index) => {
  currentSlide.value = index
  resetAutoplay()
}

const startAutoplay = () => {
  if (props.autoplay && displayImages.value.length > 1) {
    autoplayTimer = setInterval(() => {
      nextSlide()
    }, props.interval)
  }
}

const stopAutoplay = () => {
  if (autoplayTimer) {
    clearInterval(autoplayTimer)
    autoplayTimer = null
  }
}

const resetAutoplay = () => {
  stopAutoplay()
  startAutoplay()
}

onMounted(() => {
  startAutoplay()
})

onUnmounted(() => {
  stopAutoplay()
})
</script>

<style scoped>
.image-slider {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: inherit;
  overflow: hidden;
}

.slider-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.slides {
  position: relative;
  width: 100%;
  height: 100%;
}

.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slide-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.3;
  transition: opacity 0.3s;
}

.slide:hover .slide-overlay {
  opacity: 0.5;
}

.slide-icon {
  position: relative;
  font-size: 4rem;
  z-index: 2;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s;
}

.slide:hover .slide-icon {
  transform: scale(1.1);
}

/* انیمیشن اسلاید */
.slide-fade-enter-active {
  transition: all 0.6s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.4s ease-in;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: scale(1.05);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* دکمه‌های ناوبری */
.slider-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.9);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  opacity: 0;
  color: #333;
}

.image-slider:hover .slider-arrow {
  opacity: 1;
}

.slider-arrow:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.slider-arrow.prev {
  left: 1rem;
}

.slider-arrow.next {
  right: 1rem;
}

/* نقاط ناوبری */
.slider-dots {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
  z-index: 10;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid white;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s;
  padding: 0;
}

.dot:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: scale(1.2);
}

.dot.active {
  background: white;
  transform: scale(1.3);
}

/* تصویر placeholder */
.image-placeholder {
  position: relative;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder .slide-overlay {
  opacity: 0.3;
}

/* Gradient placeholder */
.gradient-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}



/* حالت تاریک */
.dark-mode .slider-arrow {
  background: rgba(0, 0, 0, 0.7);
  color: white;
}

.dark-mode .slider-arrow:hover {
  background: rgba(0, 0, 0, 0.9);
}
</style>
