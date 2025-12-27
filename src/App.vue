<template>
  <div id="app">
    <!-- Home Page -->
    <div v-if="currentPage === 'home'" class="page-content">
      <Header />
      <Hero />
      <Stats />
      <BimServices />
      <SurveyingServices />
      <About />
      <Projects />
      <CTA />
      <FeaturedArticles />
      <Certificates />
      <Team />
      <Contact id="contact" />
      <Footer />
    </div>

    <!-- Articles Archive Page -->
    <div v-else-if="currentPage === 'articles'" class="page-content">
      <Header />
      <ArticlesArchive />
      <Footer />
    </div>

    <!-- Article Detail Page -->
    <div v-else-if="currentPage === 'article-detail'" class="page-content">
      <Header />
      <ArticleDetail />
      <Footer />
    </div>

    <!-- Projects Archive Page -->
    <div v-else-if="currentPage === 'projects'" class="page-content">
      <Header />
      <ProjectsArchive />
      <Footer />
    </div>

    <!-- Project Detail Page -->
    <div v-else-if="currentPage === 'project-detail'" class="page-content">
      <Header />
      <ProjectDetail />
      <Footer />
    </div>

     <!-- Admin Pages -->
     <div v-else-if="currentPage === 'admin-login'" class="page-content">
       <AdminLogin />
     </div>

     <div v-else-if="currentPage === 'admin-dashboard'" class="page-content">
       <AdminDashboard />
     </div>

     <div v-else-if="currentPage === 'admin-content'" class="page-content">
       <AdminContentManager />
     </div>

     <div v-else-if="currentPage === 'admin-settings'" class="page-content">
       <AdminSettings />
     </div>

      <div v-else-if="currentPage === 'admin-users'" class="page-content">
        <AdminUsers />
      </div>

      <div v-else-if="currentPage === 'admin-contacts'" class="page-content">
        <AdminContacts />
      </div>
    <ScrollToTop />
    <VideoPopup ref="videoPopup" />
    <div v-if="appLoading" class="app-loader">
      <Loader />
    </div>
  </div>
</template>

<script>
import Header from './components/Header.vue'
import Hero from './components/Hero.vue'
import Stats from './components/Stats.vue'
import BimServices from './components/BimServices.vue'
import Projects from './components/Projects.vue'
import SurveyingServices from './components/SurveyingServices.vue'
import About from './components/About.vue'
import CTA from './components/CTA.vue'
import Certificates from './components/Certificates.vue'
import Licenses from './components/Licenses.vue'
import Team from './components/Team.vue'
import Contact from './components/Contact.vue'
import Footer from './components/Footer.vue'
import ScrollToTop from './components/ScrollToTop.vue'
import ArticlesArchive from './components/ArticlesArchive.vue'
import ArticleDetail from './components/ArticleDetail.vue'
import ProjectsArchive from './components/ProjectsArchive.vue'
import ProjectDetail from './components/ProjectDetail.vue'
import FeaturedArticles from './components/FeaturedArticles.vue'
import VideoPopup from './components/VideoPopup.vue'
import AdminLogin from './components/AdminLogin.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import AdminContentManager from './components/AdminContentManager.vue'
import AdminSettings from './components/AdminSettings.vue'
import AdminUsers from './components/AdminUsers.vue'
import AdminContacts from './components/AdminContacts.vue'
import Loader from './components/Loader.vue'

export default {
  name: 'App',
  components: {
    Header,
    Hero,
    Stats,
    BimServices,
    Projects,
    SurveyingServices,
    About,
    CTA,
    Certificates,
    Licenses,
    Team,
    Contact,
    Footer,
    ScrollToTop,
    ArticlesArchive,
    ArticleDetail,
    ProjectsArchive,
    ProjectDetail,
    FeaturedArticles,
    VideoPopup,
    AdminLogin,
    AdminDashboard,
    AdminContentManager,
    AdminSettings,
    AdminUsers,
    AdminContacts,
    Loader
  },
  data() {
    return {
      currentPage: 'home',
      appLoading: true
    }
  },
  provide() {
    const self = this;
    return {
      navigateTo: function(path) { return self.navigateTo(path); },
      playVideo: function(videoUrl) { return self.playVideo(videoUrl); },
      scrollTo: function(section) { return self.scrollTo(section); }
    }
  },
  mounted() {
    this.handleRouting();
    this.initIntersectionObserver();

    // Listen for popstate (browser back/forward)
    window.addEventListener('popstate', () => {
      this.handleRouting();
      this.$nextTick(() => {
        this.initIntersectionObserver();
      });
    });
  },
  methods: {
    checkAdminAuth() {
      const token = localStorage.getItem('admin_token');
      if (!token && window.location.pathname.startsWith('/admin') && !window.location.pathname.includes('/login')) {
        this.navigateTo('/admin/login');
        return false;
      }
      return true;
    },
    handleRouting() {
      const pathname = window.location.pathname;

      // Admin routes
      if (pathname === '/admin/login' || pathname === '/admin/login/') {
        this.currentPage = 'admin-login';
      } else if (pathname.startsWith('/admin')) {
        if (this.checkAdminAuth()) {
          if (pathname === '/admin' || pathname === '/admin/') {
            this.currentPage = 'admin-dashboard';
          } else if (pathname.includes('/settings')) {
            this.currentPage = 'admin-settings';
          } else if (pathname.includes('/users')) {
            this.currentPage = 'admin-users';
          } else if (pathname.includes('/contacts')) {
            this.currentPage = 'admin-contacts';
          } else {
            this.currentPage = 'admin-content';
          }
        }
      }
      // Public routes
      if (!pathname.startsWith('/admin')) {
        if (pathname.startsWith('/article/')) {
          this.currentPage = 'article-detail';
        } else if (pathname === '/articles' || pathname === '/articles/') {
          this.currentPage = 'articles';
        } else if (pathname.startsWith('/project/')) {
          this.currentPage = 'project-detail';
        } else if (pathname === '/projects-archive' || pathname === '/projects-archive/') {
          this.currentPage = 'projects';
        } else {
          this.currentPage = 'home';
        }
      }
    },
    navigateTo(path) {
      window.history.pushState(null, '', path);
      this.handleRouting();
      this.$nextTick(() => {
        this.initIntersectionObserver();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    },
    playVideo(videoUrl) {
      this.$refs.videoPopup.openPopup(videoUrl);
    },
    scrollTo(section) {
      const el = document.getElementById(section);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    },
    initIntersectionObserver() {
      // Initialize Intersection Observer for scroll-triggered animations
      // Use setTimeout to ensure DOM is fully rendered
      setTimeout(() => {
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
        const animatedElements = document.querySelectorAll('.animate-on-scroll, .animate-on-scroll-large');
        animatedElements.forEach(el => {
          observer.observe(el);
        });

        // Trigger intersection check immediately for elements already in viewport
        animatedElements.forEach(el => {
          const rect = el.getBoundingClientRect();
          if (rect.top < window.innerHeight && rect.bottom > 0) {
            el.classList.add('in-view');
            observer.unobserve(el);
          }
        });

        // Hide app loader after animations are set up
        this.appLoading = false;
      }, 650);
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
  width: 100%;
}

.page-content {
  width: 100%;
  min-height: 100vh;
}

.app-loader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* Global Styles */
.section-title {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  margin: 40px 0 30px;
  position: relative;
  padding-bottom: 5px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 50%;
  transform: translateX(50%);
  width: 60px;
  height: 2px;
  background: #87CEEB;
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
  background-color: #87CEEB;
  color: white;
}

.btn-primary:hover {
  background-color: #6BB9E8;
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
    font-size: 20px;
    margin: 25px 0 15px;
    padding-bottom: 10px;
  }

  .section-title::after {
    width: 50px;
    height: 2px;
    background: #00BFFF;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 14px;
    margin: 15px 0 10px;
    padding-bottom: 5px;
  }

  .section-title::after {
    width: 50px;
    height: 2px;
    background: #00BFFF;
  }
}
</style>
