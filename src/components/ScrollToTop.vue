<template>
  <div class="scroll-top" :class="{ active: isVisible }" @click="scrollToTop" id="scrollTop">↑</div>
</template>

<script>
export default {
  name: 'ScrollToTop',
  data() {
    return {
      isVisible: false
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.isVisible = window.scrollY > 300
    },
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    }
  }
}
</script>

<style scoped>
.scroll-top {
  position: fixed;
  bottom: 30px;
  left: 30px;
  width: 50px;
  height: 50px;
  background: #1abc9c;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  font-size: 20px;
  transition: all 0.3s;
  opacity: 0;
  pointer-events: none;
  z-index: 999;
}

.scroll-top.active {
  opacity: 1;
  pointer-events: all;
}

.scroll-top:hover {
  background: #16a085;
}

@media (max-width: 1024px) {
  .scroll-top {
    left: 20px;
    bottom: 20px;
  }
}

@media (max-width: 768px) {
  .scroll-top {
    left: 15px;
    bottom: 15px;
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .scroll-top {
    left: 12px;
    bottom: 12px;
    width: 38px;
    height: 38px;
    font-size: 14px;
  }
}
</style>
