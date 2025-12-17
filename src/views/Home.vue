<template>
  <div>
    <Navbar @toggle-theme="toggleTheme" :is-dark="isDark" />
    <Hero />
    <Gallery :show-view-all="true" />
    <Statistics />
    <Services />
    <Articles :show-view-all="true" />
    <Testimonials />
    <Certificates />
    <ContactForm />
    <Footer />
  </div>
</template>

<script setup>
import { inject } from 'vue'
import Navbar from '../components/Navbar.vue'
import Hero from '../components/Hero.vue'
import Gallery from '../components/Gallery.vue'
import Services from '../components/Services.vue'
import Statistics from '../components/Statistics.vue'
import Articles from '../components/Articles.vue'
import Testimonials from '../components/Testimonials.vue'
import Certificates from '../components/Certificates.vue'
import ContactForm from '../components/ContactForm.vue'
import Footer from '../components/Footer.vue'

// Inject theme from App.vue
const { isDark, toggleTheme } = inject('theme')
</script>
