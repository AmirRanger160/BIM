<template>
  <transition name="modal">
    <div v-if="isOpen" class="video-popup-overlay" @click.self="closePopup">
      <div class="video-popup-container">
        <button class="close-btn" @click="closePopup" aria-label="Close video">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <div class="video-wrapper">
          <video
            v-if="videoSource"
            controls
            autoplay
            muted
            class="video-element"
            @click.stop
          >
            <source :src="videoSource" type="video/mp4">
            مرورگر شما از تگ ویدیو پشتیبانی نمی‌کند.
          </video>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'VideoPopup',
  data() {
    return {
      isOpen: false,
      videoSource: null
    };
  },
  methods: {
    openPopup(videoUrl) {
      this.videoSource = videoUrl;
      this.isOpen = true;
      document.body.style.overflow = 'hidden';
    },
    closePopup() {
      this.isOpen = false;
      this.videoSource = null;
      document.body.style.overflow = '';
    }
  },
  mounted() {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && this.isOpen) {
        this.closePopup();
      }
    };
    window.addEventListener('keydown', handleEscape);
    this.cleanup = () => {
      window.removeEventListener('keydown', handleEscape);
    };
  },
  beforeUnmount() {
    if (this.cleanup) {
      this.cleanup();
    }
  }
};
</script>

<style scoped>
.video-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.video-popup-container {
  position: relative;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  background-color: #000;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: rgba(0, 0, 0, 0.6);
  border: none;
  color: #ffffff;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
  z-index: 2001;
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.9);
}

.video-wrapper {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
}

.video-element {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  outline: none;
}

/* Animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .video-popup-container,
.modal-leave-active .video-popup-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .video-popup-container,
.modal-leave-to .video-popup-container {
  transform: scale(0.95);
}

/* Responsive */
@media (max-width: 768px) {
  .video-popup-overlay {
    padding: 0.5rem;
  }

  .close-btn {
    top: 0.75rem;
    right: 0.75rem;
    width: 36px;
    height: 36px;
  }

  .close-btn svg {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 480px) {
  .video-popup-container {
    border-radius: 4px;
  }

  .close-btn {
    top: 0.5rem;
    right: 0.5rem;
    width: 32px;
    height: 32px;
  }

  .close-btn svg {
    width: 18px;
    height: 18px;
  }
}
</style>
