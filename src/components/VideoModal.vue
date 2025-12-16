<template>
  <teleport to="body">
    <div v-if="isOpen" class="video-modal-overlay" @click.self="close">
      <div class="video-modal">
        <button class="close-btn" @click="close" title="بستن">✕</button>
        
        <div class="modal-content">
          <!-- YouTube embed -->
          <iframe
            v-if="isYouTubeUrl"
            :src="getEmbedUrl"
            title="ویدیو"
            allowFullscreen
            class="video-frame"
          ></iframe>
          
          <!-- Vimeo embed -->
          <iframe
            v-else-if="isVimeoUrl"
            :src="getEmbedUrl"
            allowFullscreen
            class="video-frame"
          ></iframe>
          
          <!-- Direct video player -->
          <video
            v-else-if="isDirectVideoUrl"
            controls
            class="video-frame"
            autoplay
          >
            <source :src="video.video_url" />
            مرورگر شما از پخش ویدیو پشتیبانی نمی‌کند.
          </video>
          
          <!-- Custom HTML embed -->
          <div v-else class="custom-embed" v-html="video.video_url"></div>

          <div class="video-info-bottom">
            <h2>{{ video.title }}</h2>
            <p v-if="video.description">{{ video.description }}</p>
            <div class="video-stats">
              <span>👁️ {{ video.views }} بازدید</span>
              <span v-if="video.duration">⏱️ {{ video.duration }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  video: {
    type: Object,
    default: () => ({
      id: null,
      title: '',
      description: '',
      video_url: '',
      duration: '',
      views: 0
    })
  }
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}

// تشخیص نوع URL
const isYouTubeUrl = computed(() => {
  if (!props.video.video_url) return false
  return (
    props.video.video_url.includes('youtube.com') ||
    props.video.video_url.includes('youtu.be') ||
    props.video.video_url.includes('youtube-nocookie.com')
  )
})

const isVimeoUrl = computed(() => {
  if (!props.video.video_url) return false
  return props.video.video_url.includes('vimeo.com')
})

const isDirectVideoUrl = computed(() => {
  if (!props.video.video_url) return false
  const url = props.video.video_url.toLowerCase()
  return /\.(mp4|webm|ogg|mov)$/.test(url)
})

// تبدیل URL های معمولی به embed URL
const getEmbedUrl = computed(() => {
  const url = props.video.video_url

  // YouTube
  if (isYouTubeUrl.value) {
    // فرمت‌های مختلف YouTube
    const youtubeRegex =
      /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube-nocookie\.com\/embed\/)([^"&?\s]{11})/
    const match = url.match(youtubeRegex)
    if (match && match[1]) {
      return `https://www.youtube.com/embed/${match[1]}`
    }
    // اگر قبلاً embed URL است
    if (url.includes('youtube.com/embed/')) {
      return url
    }
    return url
  }

  // Vimeo
  if (isVimeoUrl.value) {
    const vimeoRegex = /(?:vimeo\.com\/)(\d+)/
    const match = url.match(vimeoRegex)
    if (match && match[1]) {
      return `https://player.vimeo.com/video/${match[1]}`
    }
    if (url.includes('player.vimeo.com')) {
      return url
    }
    return url
  }

  return url
})
</script>

<style scoped>
.video-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.video-modal {
  position: relative;
  background: #000;
  border-radius: 1rem;
  overflow: hidden;
  max-width: 90vw;
  max-height: 90vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.4s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 10;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.8);
  transform: scale(1.1);
}

.modal-content {
  display: flex;
  flex-direction: column;
  overflow: auto;
  max-height: 90vh;
}

.video-frame {
  width: 100%;
  aspect-ratio: 16 / 9;
  border: none;
  background: #000;
}

.custom-embed {
  width: 100%;
  aspect-ratio: 16 / 9;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 1.2rem;
}

.video-info-bottom {
  padding: 1.5rem;
  background: #111;
  color: white;
}

.video-info-bottom h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  line-height: 1.3;
}

.video-info-bottom p {
  margin: 0 0 1rem;
  color: #aaa;
  line-height: 1.5;
  max-height: 6rem;
  overflow: auto;
}

.video-stats {
  display: flex;
  gap: 1.5rem;
  font-size: 0.95rem;
  color: #999;
}

/* Responsive */
@media (max-width: 768px) {
  .video-modal-overlay {
    padding: 0;
  }

  .video-modal {
    max-width: 100vw;
    max-height: 100vh;
    border-radius: 0;
  }

  .close-btn {
    width: 2rem;
    height: 2rem;
    font-size: 1.2rem;
    top: 0.75rem;
    right: 0.75rem;
  }

  .video-frame {
    aspect-ratio: auto;
    min-height: 50vh;
  }

  .video-info-bottom {
    padding: 1rem;
  }

  .video-info-bottom h2 {
    font-size: 1.2rem;
  }

  .video-stats {
    gap: 1rem;
    font-size: 0.85rem;
  }
}

@media (max-height: 500px) {
  .video-modal-overlay {
    align-items: flex-start;
    padding-top: 0;
  }

  .video-modal {
    max-height: 100vh;
    border-radius: 0;
  }

  .video-frame {
    aspect-ratio: 16 / 9;
  }
}
</style>
