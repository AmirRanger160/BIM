import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import GalleryArchive from '../views/GalleryArchive.vue'
import ArticlesArchive from '../views/ArticlesArchive.vue'
import AdminLogin from '../views/AdminLogin.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminArticles from '../views/AdminArticles.vue'
import AdminGallery from '../views/AdminGallery.vue'
import AdminTestimonials from '../views/AdminTestimonials.vue'
import AdminContacts from '../views/AdminContacts.vue'
import AdminSliders from '../views/AdminSliders.vue'
import AdminLayout from '../components/AdminLayout.vue'

// Guard برای احراز هویت ادمین
const requireAdminAuth = (to, from, next) => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    next()
  } else {
    next('/admin/login')
  }
}

import Welcome from '../views/Welcome.vue'

const routes = [
  {
    path: '/welcome',
    name: 'Welcome',
    component: Welcome
  },
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/gallery',
    name: 'GalleryArchive',
    component: GalleryArchive
  },
  {
    path: '/articles',
    name: 'ArticlesArchive',
    component: ArticlesArchive
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLogin
  },
  {
    path: '/admin',
    component: AdminLayout,
    beforeEnter: requireAdminAuth,
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard
      },
      {
        path: 'articles',
        name: 'AdminArticles',
        component: AdminArticles
      },
      {
        path: 'gallery',
        name: 'AdminGallery',
        component: AdminGallery
      },
      {
        path: 'testimonials',
        name: 'AdminTestimonials',
        component: AdminTestimonials
      },
      {
        path: 'contacts',
        name: 'AdminContacts',
        component: AdminContacts
      },
      {
        path: 'sliders',
        name: 'AdminSliders',
        component: AdminSliders
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

export default router
