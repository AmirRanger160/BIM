<template>
  <div id="app">
    <Header />
    <Hero />
    <Stats />
    <BimServices />
    <SurveyingServices />
    <About />
    <CTA />
    <Certificates />
    <Licenses />
    <Team />
    <Contact />
    <Footer />
    <ScrollToTop />
  </div>
</template>

<script>
import Header from './components/Header.vue'
import Hero from './components/Hero.vue'
import Stats from './components/Stats.vue'
import BimServices from './components/BimServices.vue'
import SurveyingServices from './components/SurveyingServices.vue'
import About from './components/About.vue'
import CTA from './components/CTA.vue'
import Certificates from './components/Certificates.vue'
import Licenses from './components/Licenses.vue'
import Team from './components/Team.vue'
import Contact from './components/Contact.vue'
import Footer from './components/Footer.vue'
import ScrollToTop from './components/ScrollToTop.vue'

export default {
  name: 'App',
  components: {
    Header,
    Hero,
    Stats,
    BimServices,
    SurveyingServices,
    About,
    CTA,
    Certificates,
    Licenses,
    History,
    Team,
    Contact,
    Footer,
    ScrollToTop
  },
  mounted() {
    this.initIntersectionObserver();
  },
  methods: {
    initIntersectionObserver() {
      // Initialize Intersection Observer for scroll-triggered animations
      const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      };

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            observer.unobserve(entry.target);
          }
        });
      }, observerOptions);

      // Observe all elements with animate-on-scroll class
      document.querySelectorAll('.animate-on-scroll, .animate-on-scroll-large').forEach(el => {
        observer.observe(el);
      });
    }
  }
}
</script>

<style>
@import './styles/animations.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Vazirmatn', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.8;
  color: #333;
  direction: rtl;
  text-align: right;
}

#app {
  font-family: 'Vazirmatn', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  direction: rtl;
  text-align: right;
}

/* Global Styles */
.section-title {
  text-align: center;
  font-size: 32px;
  font-weight: bold;
  margin: 60px 0 50px;
  position: relative;
  padding-bottom: 10px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 50%;
  transform: translateX(50%);
  width: 60px;
  height: 1px;
  background: #1abc9c;
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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateZ(0);
  backface-visibility: hidden;
}

.btn:hover {
  transform: scale(1.02);
}

.btn:active {
  transform: scale(0.98);
}

.btn-primary {
  background-color: #1abc9c;
  color: white;
}

.btn-primary:hover {
  background-color: #16a085;
}

/* Responsive */
@media (max-width: 1024px) {
  .section-title {
    font-size: 28px;
    margin: 40px 0 30px;
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 22px;
    margin: 30px 0 20px;
    padding-bottom: 15px;
  }

  .section-title::after {
    width: 50px;
    height: 2px;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 16px;
    margin: 20px 0 15px;
    padding-bottom: 10px;
  }

  .section-title::after {
    width: 50px;
    height: 2px;
  }
}
</style>
