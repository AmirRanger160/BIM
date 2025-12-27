<template>
  <header class="header">
    <div class="header-content">
      <!-- Logo -->
      <div class="logo-container" @click="navigateHome">
        <img src="https://b1m.ir/wp-content/uploads/2021/05/21b1m-logo-450.png" alt="logo" class="logo">
      </div>

      <!-- Desktop Navigation -->
      <nav class="nav-desktop">
        <ul class="nav-list">
          <li><a href="#" @click.prevent="handleNavigation('about')">درباره</a></li>
          <li><a href="#" @click.prevent="handleNavigation('contact')">تماس</a></li>
          <li><a href="#" @click.prevent="handleNavigation('/articles')">مقالات</a></li>
          <li><a href="#" @click.prevent="handleNavigation('/projects-archive')">پروژه‌ها</a></li>
          <li><a href="#" @click.prevent="handleNavigation('surveying')">خدمات نقشه‌برداری</a></li>
          <li><a href="#" @click.prevent="handleNavigation('bim')">خدمات BIM</a></li>
          <li><a href="#" @click.prevent="handleNavigation('/')">صفحه اول</a></li>
        </ul>
      </nav>

      <!-- Mobile Hamburger Button -->
      <button 
        class="hamburger" 
        @click="toggleMobileMenu()"
        aria-label="Open navigation menu"
        :class="{active: mobileMenuOpen}"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>

    <!-- Mobile Navigation Overlay -->
    <transition name="overlay">
      <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu()"></div>
    </transition>

    <!-- Mobile Navigation Menu -->
    <transition name="slide">
      <nav v-if="mobileMenuOpen" class="nav-mobile">
        <ul class="nav-list-mobile">
          <li><a href="#" @click.prevent="handleNavClick('/')">صفحه اول</a></li>
          <li><a href="#" @click.prevent="handleNavClick('bim')">خدمات BIM</a></li>
          <li><a href="#" @click.prevent="handleNavClick('surveying')">خدمات نقشه‌برداری</a></li>
          <li><a href="#" @click.prevent="handleNavClick('/projects-archive')">پروژه‌ها</a></li>
          <li><a href="#" @click.prevent="handleNavClick('/articles')">مقالات</a></li>
          <li><a href="#" @click.prevent="handleNavClick('about')">درباره</a></li>
          <li><a href="#" @click.prevent="handleNavClick('contact')">تماس</a></li>
        </ul>
      </nav>
    </transition>
  </header>
</template>

<script>
export default {
  name: 'Header',
  inject: ['navigateTo'],
  data() {
    return {
      mobileMenuOpen: false
    };
  },
  methods: {
    navigateHome() {
      this.navigateTo('/');
      this.closeMobileMenu();
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false;
    },
    handleNavigation(path) {
      // If navigating to a section on the home page
      if (path === '/' || ['bim', 'surveying', 'about', 'contact'].includes(path)) {
        // If already on home, scroll to section
        if (this.$root.currentPage === 'home') {
          const element = document.getElementById(path);
          if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
          }
        } else {
          // Navigate to home first
          this.navigateTo('/');
        }
      } else {
        // Navigate to page (projects or articles archive)
        this.navigateTo(path);
      }
    },
    handleNavClick(path) {
      this.closeMobileMenu();
      this.handleNavigation(path);
    }
  },
  mounted() {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        this.closeMobileMenu();
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
.header {
  position: sticky;
  top: 0;
  width: 100%;
  background-color: #ffffff;
  border-bottom: 1px solid #f0f0f0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  flex-direction: row-reverse;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.logo-container {
  cursor: pointer;
  transition: opacity 0.3s ease;
  flex-shrink: 0;
}

.logo-container:hover {
  opacity: 0.7;
}

.logo {
  height: 50px;
  width: auto;
  object-fit: contain;
}

/* Desktop Navigation */
.nav-desktop {
  display: none;
}

@media (min-width: 1025px) {
  .nav-desktop {
    display: block;
    flex: 1;
  }

  .nav-list {
    display: flex;
    flex-direction: row-reverse;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 2rem;
    justify-content: center;
    margin-right: 1rem;
  }

  .nav-list a {
    text-decoration: none;
    color: #333333;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.3s ease;
    position: relative;
    padding-bottom: 4px;
  }

  .nav-list a:hover {
    color: #87CEEB;
  }

  .nav-list a::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background-color: #87CEEB;
    transform: scaleX(0);
    transform-origin: right;
    transition: transform 0.3s ease;
  }

  .nav-list a:hover::after {
    transform: scaleX(1);
  }
}

/* Mobile Hamburger */
.hamburger {
  display: flex;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  gap: 6px;
  align-items: flex-end;
  flex-shrink: 0;
}

.hamburger span {
  width: 24px;
  height: 2px;
  background-color: #333333;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: right;
}

.hamburger.active span:first-child {
  transform: rotate(-45deg) translateY(12px);
}

.hamburger.active span:nth-child(2) {
  opacity: 0;
}

.hamburger.active span:last-child {
  transform: rotate(45deg) translateY(-12px);
}

@media (min-width: 1025px) {
  .hamburger {
    display: none;
  }
}

/* Mobile Navigation */
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 999;
}

.nav-mobile {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  background-color: #ffffff;
  border-bottom: 1px solid #f0f0f0;
  z-index: 1001;
}

.nav-list-mobile {
  display: flex;
  flex-direction: column-reverse;
  list-style: none;
  margin: 0;
  padding: 0.5rem 0;
  gap: 0;
}

.nav-list-mobile li {
  border-bottom: 1px solid #f0f0f0;
}

.nav-list-mobile li:last-child {
  border-bottom: none;
}

.nav-list-mobile a {
  display: block;
  padding: 0.75rem 2rem;
  text-decoration: none;
  color: #333333;
  font-size: 0.95rem;
  font-weight: 500;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.nav-list-mobile a:active,
.nav-list-mobile a:hover {
  background-color: #f5f5f5;
  color: #87CEEB;
}

/* Transitions */
.overlay-enter-active,
.overlay-leave-active {
  transition: opacity 0.3s ease;
}

.overlay-enter-from,
.overlay-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateY(-100%);
}

/* Responsive */
@media (max-width: 1024px) {
  .header-content {
    padding: 1rem 1.5rem;
  }
}

@media (max-width: 768px) {
  .header-content {
    padding: 0.75rem 1rem;
  }

  .logo {
    font-size: 1.25rem;
  }

  .nav-mobile {
    top: 50px;
  }

  .nav-list-mobile a {
    padding: 0.75rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .header-content {
    padding: 0.5rem 1rem;
  }

  .logo {
    font-size: 1.1rem;
  }

  .hamburger {
    padding: 0.25rem;
  }

  .hamburger span {
    width: 20px;
    height: 1.5px;
  }

  .nav-list-mobile a {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}
</style>
