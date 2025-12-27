<template>
  <section class="hero" id="home">
    <video class="hero-video" autoplay muted loop>
      <source src="/video-1080-2.mp4" type="video/mp4">
    </video>
    <div class="hero-content">
      <h1 class="fade-in">راهکارهای جغرافیایی<br>با کیفیت بالا</h1>
      <p class="fade-in" style="animation-delay: 0.2s;">شرکت ما خدمات مختلفی و راهکارهای جغرافیایی برای کسب‌وکارهای سراسر جهان ارائه می‌دهد.</p>
      <div class="hero-buttons">
        <button class="play-btn fade-in" style="animation-delay: 0.4s;" @click="playVideo">▶</button>
        <button class="btn btn-primary fade-in" style="animation-delay: 0.4s;" @click="scrollTo('contact')">تماس با ما</button>
      </div>
    </div>
    <video-popup ref="videoPopup"></video-popup>
  </section>
</template>

<script>
import VideoPopup from './VideoPopup.vue'

export default {
  name: 'Hero',
  components: {
    VideoPopup
  },
  inject: ['scrollTo'],
  mounted() {
    const video = this.$el.querySelector('.hero-video')
    console.log('Hero video element:', video)
    if (video) {
      video.addEventListener('loadeddata', () => console.log('Video loaded successfully'))
      video.addEventListener('error', (e) => console.error('Video failed to load:', e))
      video.addEventListener('canplay', () => console.log('Video can play'))
      console.log('Video src:', video.src)
    }
  },
  methods: {
    playVideo() {
      this.$refs.videoPopup.openPopup('/video-1080-2.mp4')
    }
  }
}
</script>

<style scoped>
.hero {
  position: relative;
  color: white;
  padding: 150px 50px;
  text-align: center;
  min-height: 710px;
  display: flex;
  align-items: center;
  overflow: hidden;
  justify-content: center;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1;
}

.hero-video {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  z-index: 0;
  object-fit: cover;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-content h1 {
  font-size: 52px;
  font-weight: bold;
  margin-bottom: 5px;
  line-height: 1.2;
  max-width: 700px;
  text-align: right;
}

.hero-content p {
  font-size: 20px;
  margin-bottom: 40px;
  max-width: 700px;
  line-height: 1.6;
  text-align: right;
}

.hero-buttons {
  display: flex;
  gap: 30px;
  align-items: center;
  flex-direction: row-reverse;
  justify-content: flex-end;
}

.btn {
  padding: 10px 30px;
  border: none;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  font-size: 12px;
  font-weight: bold;
  white-space: nowrap;
  font-family: inherit;
}

.btn-primary {
  background-color: #00BFFF;
  color: white;
}

.btn-primary:hover {
  background-color: #0099CC;
}

.play-btn {
  width: 55px;
  height: 55px;
  background-color: rgba(0, 0, 0, 0.968);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 18px;
  color: white;
  border: none;
}

.play-btn:hover {
  background: rgba(18, 18, 18, 0.905);
  transform: scale(1.1);
  box-shadow: 0 8px 30px rgba(26, 188, 156, 0.5);
}

@media (max-width: 1024px) {
  .hero {
    padding: 100px 30px;
    min-height: 500px;
  }

  .hero-content h1 {
    font-size: 42px;
  }

  .hero-content p {
    font-size: 16px;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 60px 20px;
    min-height: 400px;
    text-align: center;
    justify-content: center;
  }

  .hero-content h1 {
    font-size: 28px;
    margin-bottom: 15px;
    max-width: 100%;
  }

  .hero-content p {
    font-size: 14px;
    margin-bottom: 30px;
    max-width: 100%;
  }

  .hero-buttons {
    flex-direction: column;
    gap: 15px;
    justify-content: center;
  }

  .btn {
    padding: 12px 30px;
    font-size: 12px;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .play-btn {
    width: 60px;
    height: 60px;
    font-size: 22px;
    min-height: 44px;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 40px 15px;
    min-height: 300px;
  }

  .hero-content h1 {
    font-size: 22px;
    margin-bottom: 12px;
  }

  .hero-content p {
    font-size: 12px;
    margin-bottom: 20px;
  }

  .hero-buttons {
    flex-direction: column;
    gap: 10px;
  }

  .btn {
    padding: 10px 25px;
    font-size: 11px;
    min-height: 44px;
  }

  .play-btn {
    width: 55px;
    height: 55px;
    font-size: 20px;
    min-height: 44px;
  }
}
</style>
