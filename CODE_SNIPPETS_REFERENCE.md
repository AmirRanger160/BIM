# Animation Implementation Code Reference

## Quick Copy-Paste Guide for Adding Animations to New Components

### 1. Basic Fade-In on Page Load
```vue
<template>
  <div class="fade-in">Content appears on load</div>
</template>

<style scoped>
/* No CSS needed - animation comes from animations.css import */
</style>
```

### 2. Staggered Fade-In (Multiple Elements)
```vue
<template>
  <h2 class="fade-in">Heading</h2>
  <p class="fade-in" style="animation-delay: 0.2s;">Paragraph 1</p>
  <p class="fade-in" style="animation-delay: 0.4s;">Paragraph 2</p>
  <button class="btn btn-primary fade-in" style="animation-delay: 0.6s;">
    Button
  </button>
</template>
```

### 3. Scroll-Triggered Animation
```vue
<template>
  <!-- Add animate-on-scroll class to any element -->
  <section class="my-section">
    <h2 class="section-title animate-on-scroll">Title</h2>
    <div class="animate-on-scroll">Card 1</div>
    <div class="animate-on-scroll">Card 2</div>
    <div class="animate-on-scroll">Card 3</div>
  </section>
</template>

<!-- The Intersection Observer in App.vue's mounted() hook handles the rest -->
```

### 4. Hover Scale Effect on Cards
```vue
<style scoped>
.card {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
              box-shadow 0.3s ease-out;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}
</style>
```

### 5. Hover Image Zoom
```vue
<style scoped>
.card img {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover img {
  transform: scale(1.03);
}
</style>
```

### 6. Enhanced Button Hover
```vue
<style scoped>
.btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateZ(0);
  backface-visibility: hidden;
}

.btn:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.btn:active {
  transform: scale(0.98);
}
</style>
```

### 7. Focus State for Form Inputs
```vue
<style scoped>
input, textarea {
  border: 2px solid #ddd;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

input:focus, textarea:focus {
  outline: none;
  border-color: #1abc9c;
  box-shadow: 0 0 0 3px rgba(26, 188, 156, 0.1);
}
</style>
```

### 8. Underline Animation on Links
```vue
<style scoped>
a {
  position: relative;
  text-decoration: none;
  color: #333;
  transition: color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

a::after {
  content: '';
  position: absolute;
  bottom: -5px;
  width: 0;
  height: 2px;
  background: #1abc9c;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

a:hover {
  color: #1abc9c;
}

a:hover::after {
  width: 100%;
}
</style>
```

### 9. RTL-Compatible Menu Slide (Right Side)
```vue
<style scoped>
.mobile-menu {
  position: fixed;
  right: 0;  /* RTL: right not left */
  top: 0;
  width: 100%;
  height: 100vh;
  background: white;
  transform: translate3d(100%, 0, 0);  /* RTL: slide from right */
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.mobile-menu.open {
  transform: translate3d(0, 0, 0);
}
</style>
```

### 10. Hamburger Icon Animation
```vue
<style scoped>
.hamburger {
  background: none;
  border: none;
  display: flex;
  flex-direction: column;
  gap: 5px;
  cursor: pointer;
  padding: 8px;
}

.hamburger-line {
  width: 24px;
  height: 2.5px;
  background: #333;
  border-radius: 2px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: center;
}

/* Active state */
.hamburger.active .hamburger-line:first-child {
  transform: rotate(45deg) translateY(12px);
}

.hamburger.active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.hamburger.active .hamburger-line:last-child {
  transform: rotate(-45deg) translateY(-12px);
}
</style>
```

---

## Key Animation Properties Cheat Sheet

### Duration & Easing
```css
/* Fast micro-interactions */
transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);

/* Standard interactions */
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* Slower, more dramatic */
transition: all 0.6s ease-out;
```

### GPU-Accelerated Transforms
```css
/* GOOD - No layout shift */
transform: translateY(-8px);
transform: scale(1.02);
transform: translate3d(100%, 0, 0);
transform: rotate(45deg);
opacity: 0.5;

/* BAD - Layout shift, jank */
left: -8px;
right: 0;
width: 102%;
padding: 10px;
height: 50px;
```

### Common Cubic-Bezier Values
```css
ease-out:           cubic-bezier(0, 0, 0.2, 1)
ease-in-out:        cubic-bezier(0.4, 0, 0.2, 1)
ease-in:            cubic-bezier(0.4, 0, 1, 1)
sharp-ease-out:     cubic-bezier(0.33, 0.66, 0.66, 1)
bounce-ease-out:    cubic-bezier(0.34, 1.56, 0.64, 1)
```

### Shadow Progression
```css
/* Rest state */
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

/* Hover state */
box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);

/* Active state */
box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
```

---

## Intersection Observer Pattern

### Basic Setup (in mounted() hook)
```javascript
mounted() {
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

  document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el);
  });
}
```

### CSS for Observer Pattern
```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(30px);
}

.animate-on-scroll.in-view {
  animation: slideUp 0.6s ease-out forwards;
}

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## Mobile Responsive Breakpoints

### Tablet (≤1024px)
```css
@media (max-width: 1024px) {
  /* Reduce gaps and padding */
  gap: 30px;
  padding: 40px 30px;
  
  /* Adjust font sizes */
  font-size: 14px;
}
```

### Mobile (≤768px)
```css
@media (max-width: 768px) {
  /* Stack grids */
  grid-template-columns: 1fr;
  
  /* Hide desktop elements */
  display: none;
  
  /* Show mobile elements */
  display: block;
  
  /* Optimize spacing */
  padding: 30px 20px;
  gap: 20px;
  
  /* Ensure touch targets */
  min-height: 44px;
}
```

### Extra Small (≤480px)
```css
@media (max-width: 480px) {
  /* Minimal padding */
  padding: 20px 15px;
  
  /* Compact spacing */
  gap: 15px;
  
  /* Responsive fonts */
  font-size: 12px;
}
```

### Grid Layout Examples
```css
/* Desktop: 3 columns */
grid-template-columns: repeat(3, 1fr);

/* Tablet: 2 columns */
@media (max-width: 1024px) {
  grid-template-columns: repeat(2, 1fr);
}

/* Mobile: 1 column */
@media (max-width: 768px) {
  grid-template-columns: 1fr;
}

/* Extra small: 2 columns */
@media (max-width: 480px) {
  grid-template-columns: repeat(2, 1fr);
}
```

---

## Performance Optimization Checklist

### Before Adding Animation
```
☐ Only animate transform and opacity
☐ Use cubic-bezier(0.4, 0, 0.2, 1) for smoothness
☐ Keep duration 0.2s - 0.8s
☐ Add will-change: transform, opacity
☐ Test in DevTools Performance tab
☐ Verify 60fps on average device
```

### Debugging Animations
```javascript
// Chrome DevTools Console
// Check if element has animation
console.log(window.getComputedStyle(element).animation);

// Check if Intersection Observer is supported
console.log('IntersectionObserver' in window);

// Monitor animation performance
performance.mark('animation-start');
// ... perform animation ...
performance.mark('animation-end');
performance.measure('animation-duration', 'animation-start', 'animation-end');
```

---

## Color Palette Reference

```css
:root {
  --primary: #1abc9c;      /* Teal - hover states */
  --primary-dark: #16a085; /* Dark teal - active states */
  --text: #333;            /* Dark text */
  --text-secondary: #2a2929;
  --background: #f5f5f5;   /* Light gray background */
  --border: #ddd;          /* Light borders */
  --success: #27ae60;      /* Green */
  --shadow-light: rgba(0, 0, 0, 0.05);
  --shadow-medium: rgba(0, 0, 0, 0.1);
  --shadow-dark: rgba(0, 0, 0, 0.15);
}
```

### Usage in Transitions
```css
.btn {
  background: var(--primary);
  transition: background 0.3s ease-out, 
              box-shadow 0.3s ease-out;
}

.btn:hover {
  background: var(--primary-dark);
  box-shadow: 0 8px 16px rgba(26, 188, 156, 0.3);
}
```

---

## Common Mistakes to Avoid

### ❌ DON'T
```css
/* Causes layout shift */
transition: padding 0.3s;
transition: margin 0.3s;
transition: width 0.3s;
transition: height 0.3s;
transition: left 0.3s;

/* Too slow */
transition: all 2s;

/* Not GPU accelerated */
transition: box-shadow 0.3s, left 0.3s;

/* Wrong timing */
transition: all 0s;
```

### ✅ DO
```css
/* GPU accelerated */
transition: transform 0.3s, opacity 0.3s;

/* Right speed */
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* Specific timing */
transition: color 0.3s, 
            box-shadow 0.3s, 
            transform 0.3s;

/* Always define duration */
transition: all 0.3s;
```

---

**Last Updated:** December 23, 2025
**Version:** 1.0 - Final Release
