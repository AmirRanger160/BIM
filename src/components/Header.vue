<template>
  <header>
    <div class="header-container">
      <div class="logo">geo<span style="color: #7cb342;">biro</span></div>
      
      <!-- Desktop Navigation -->
      <nav class="nav-desktop">
        <a 
          href="#" 
          @click.prevent="handleNavigation('/')"
          :class="{ active: isActive('home') }"
        >صفحه اول</a>
        <a 
          href="#" 
          @click.prevent="handleNavClick({id: 'bim'})"
          :class="{ active: isActive('home') }"
        >خدمات BIM</a>
        <a 
          href="#" 
          @click.prevent="handleNavClick({id: 'surveying'})"
          :class="{ active: isActive('home') }"
        >خدمات نقشه‌برداری</a>
        <a 
          href="#" 
          @click.prevent="handleNavigation('/projects-archive')"
          :class="{ active: isActive('projects') }"
        >پروژه‌ها</a>
        <a 
          href="#" 
          @click.prevent="handleNavigation('/articles')"
          :class="{ active: isActive('articles') }"
        >مقالات</a>
        <a 
          href="#" 
          @click.prevent="handleNavClick({id: 'about'})"
          :class="{ active: isActive('home') }"
        >درباره</a>
        <a 
          href="#" 
          @click.prevent="handleNavClick({id: 'contact'})"
          :class="{ active: isActive('home') }"
        >تماس</a>
      </nav>

      <!-- Mobile Hamburger Button -->
      <button 
        class="hamburger" 
        :class="{ active: mobileMenuOpen }"
        @click="toggleMobileMenu"
        aria-label="Toggle navigation menu"
      >
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </button>
    </div>

    <!-- Mobile Navigation Overlay -->
    <transition name="overlay-fade">
      <div 
        v-if="mobileMenuOpen" 
        class="mobile-overlay"
        @click="closeMobileMenu"
      ></div>
    </transition>

    <!-- Mobile Navigation Menu -->
    <nav v-if="mobileMenuOpen" class="nav-mobile mobile-menu">
      <a 
        href="#" 
        @click.prevent="handleNavigation('/')"
        :class="{ active: isActive('home') }"
      >صفحه اول</a>
      <a 
        href="#" 
        @click.prevent="handleNavClick({id: 'bim'})"
        :class="{ active: isActive('home') }"
      >خدمات BIM</a>
      <a 
        href="#" 
        @click.prevent="handleNavClick({id: 'surveying'})"
        :class="{ active: isActive('home') }"
      >خدمات نقشه‌برداری</a>
      <a 
        href="#" 
        @click.prevent="handleNavigation('/projects-archive')"
        :class="{ active: isActive('projects') }"
      >پروژه‌ها</a>
      <a 
        href="#" 
        @click.prevent="handleNavigation('/articles')"
        :class="{ active: isActive('articles') }"
      >مقالات</a>
      <a 
        href="#" 
        @click.prevent="handleNavClick({id: 'about'})"
        :class="{ active: isActive('home') }"
      >درباره</a>
      <a 
        href="#" 
        @click.prevent="handleNavClick({id: 'contact'})"
        :class="{ active: isActive('home') }"
      >تماس</a>
    </nav>
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
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false;
    },
    handleNavigation(path) {
      this.mobileMenuOpen = false;
      this.navigateTo(path);
    },
    isActive(page) {
      return this.$root.currentPage === page;
    },
    handleNavClick(args) {
      const target = document.querySelector(`#${args.id}`);
      if (target) {
        this.mobileMenuOpen = false;
        target.scrollIntoView({
          behavior: 'smooth'
        });
      }
    }
  },
  mounted() {
    // Close mobile menu on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.mobileMenuOpen) {
        this.closeMobileMenu();
      }
    });
  }
}
</script>

<style scoped>
header {
  background: #fff;
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 50px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #1abc9c;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: skewX(-3deg);
}

.nav-desktop {
  display: flex;
  flex-direction: row-reverse;
  gap: 30px;
}

.nav-desktop a,
.nav-mobile a {
  text-decoration: none;
  color: #333;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  transform: skewX(-2deg);
}

.nav-desktop a::after {
  content: '';
  position: absolute;
  bottom: -5px;
  width: 0;
  height: 2px;
  background: #1abc9c;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-desktop a:hover {
  color: #1abc9c;
}

.nav-desktop a:hover::after {
  width: 100%;
}

.nav-desktop a.active {
  color: #1abc9c;
  font-weight: 600;
}

.nav-desktop a.active::after {
  width: 100%;
}

/* Hamburger Menu Button */
.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  margin: 0;
  z-index: 1001;
}

.hamburger-line {
  display: block;
  width: 24px;
  height: 2.5px;
  background: #333;
  border-radius: 2px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: center;
}

/* Mobile Navigation */
.nav-mobile {
  position: fixed;
  right: 0;
  top: 69px;
  height: calc(100vh - 69px);
  width: 100%;
  background: #fff;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 0;
  z-index: 999;
  border-top: 1px solid #e0e0e0;
}

.nav-mobile a {
  padding: 15px 20px;
  display: block;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.2s;
}

.nav-mobile a:hover {
  background: #f5f5f5;
  color: #1abc9c;
}

.nav-mobile a.active {
  background: #1abc9c;
  color: white;
  font-weight: 600;
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: transparent;
  z-index: 998;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .header-container {
    padding: 15px 30px;
  }

  .logo {
    font-size: 20px;
  }

  .nav-desktop {
    gap: 20px;
  }

  .nav-desktop a {
    font-size: 12px;
  }
}

@media (max-width: 768px) {
  .header-container {
    padding: 15px 20px;
  }

  .logo {
    font-size: 18px;
  }

  /* Show hamburger menu on mobile */
  .hamburger {
    display: flex;
  }

  /* Hide desktop navigation on mobile */
  .nav-desktop {
    display: none;
  }

  .nav-mobile {
    top: 63px;
    height: calc(100vh - 63px);
  }

  .nav-mobile a {
    padding: 16px 20px;
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .header-container {
    padding: 12px 15px;
  }

  .logo {
    font-size: 16px;
  }

  .hamburger-line {
    width: 22px;
    height: 2px;
  }

  .nav-mobile {
    top: 59px;
    height: calc(100vh - 59px);
  }

  .nav-mobile a {
    padding: 14px 16px;
    font-size: 15px;
    min-height: 44px;
  }
}

/* Fade animation for overlay */
.overlay-fade-enter-active,
.overlay-fade-leave-active {
  transition: opacity 0.3s ease-out;
}

.overlay-fade-enter-from,
.overlay-fade-leave-to {
  opacity: 0;
}
</style>
