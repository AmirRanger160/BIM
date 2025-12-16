import { createRouter, createWebHistory } from 'vue-router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import Home from '../views/Home.vue'
import MediaArchive from '../views/MediaArchive.vue'
import ArticleDetailPage from '../views/ArticleDetailPage.vue'
import ProjectDetailPage from '../views/ProjectDetailPage.vue'
import GalleryArchive from '../views/GalleryArchive.vue'
import ArticlesArchive from '../views/ArticlesArchive.vue'
import AdminLogin from '../views/AdminLogin.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminArticles from '../views/AdminArticles.vue'
import AdminGallery from '../views/AdminGallery.vue'
import AdminTestimonials from '../views/AdminTestimonials.vue'
import AdminContacts from '../views/AdminContacts.vue'
import AdminSliders from '../views/AdminSliders.vue'
import AdminCertificates from '../views/AdminCertificates.vue'
import AdminComments from '../views/AdminComments.vue'
import AdminVideos from '../views/AdminVideos.vue'
import AdminReports from '../views/AdminReports.vue'
import AdminUsers from '../views/AdminUsers.vue'
import AdminLayout from '../components/AdminLayout.vue'
import { logVisit } from '../api/services'

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
    component: Home,
    meta: {
      title: 'مهندسین مشاور دانش‌بنیان BIM | مدل‌سازی اطلاعات ساختمان',
      description: 'شرکت مهندسین مشاور دانش‌بنیان BIM ارائه‌دهنده خدمات مدل‌سازی اطلاعات ساختمان (BIM)، طراحی معماری و سازه، تاسیسات مکانیکی و الکتریکی'
    }
  },
  {
    path: '/media',
    name: 'MediaArchive',
    component: MediaArchive,
    meta: {
      title: 'مقالات و گالری | مهندسین مشاور دانش‌بنیان BIM',
      description: 'مقالات تخصصی BIM، آموزش‌های مدل‌سازی اطلاعات ساختمان و گالری پروژه‌های انجام شده'
    }
  },
  {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: ArticleDetailPage,
    meta: {
      title: 'مقاله | مهندسین مشاور دانش‌بنیان BIM',
      description: 'مقالات تخصصی در زمینه مدل‌سازی اطلاعات ساختمان'
    }
  },
  {
    path: '/project/:id',
    name: 'ProjectDetail',
    component: ProjectDetailPage,
    meta: {
      title: 'پروژه | گالری مهندسین مشاور BIM',
      description: 'نمونه کارها و پروژه‌های انجام شده با فناوری BIM'
    }
  },
  {
    path: '/gallery',
    redirect: '/media?tab=gallery'
  },
  {
    path: '/articles',
    redirect: '/media?tab=articles'
  },
  // Keep old routes for backward compatibility (will be redirected)
  {
    path: '/gallery-old',
    name: 'GalleryArchive',
    component: GalleryArchive
  },
  {
    path: '/articles-old',
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
        path: 'reports',
        name: 'AdminReports',
        component: AdminReports
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
      },
      {
        path: 'certificates',
        name: 'AdminCertificates',
        component: AdminCertificates
      },
      {
        path: 'comments',
        name: 'AdminComments',
        component: AdminComments
      },
      {
        path: 'videos',
        name: 'AdminVideos',
        component: AdminVideos
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers
      },
      {
        path: 'services',
        name: 'AdminServices',
        component: () => import('../views/AdminServices.vue')
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

// Configure a thin, fast progress bar
NProgress.configure({ showSpinner: false, trickleSpeed: 120 })

router.beforeEach((to, from, next) => {
  NProgress.start()
  next()
})

router.afterEach((to) => {
  NProgress.done()
  // Log visits only for غیر-ادمین صفحات
  if (!to.path.startsWith('/admin')) {
    logVisit({ path: to.fullPath, referer: document.referrer })
  }
})

router.onError(() => NProgress.done())

export default router
