<template>
  <section id="gallery" class="gallery-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">نمونه کارهای ما</h2>
        <p class="section-subtitle">پورتفولیو و پروژه‌های موفق ما</p>
        <router-link v-if="showViewAll" to="/gallery" class="view-all-btn">
          مشاهده همه پروژه‌ها
          <span class="btn-icon">→</span>
        </router-link>
      </div>
      
      <!-- Search and Filter -->
      <div class="gallery-controls">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="جستجو در پروژه‌ها..."
            class="search-input"
          />
        </div>
        
        <div class="filter-buttons">
          <button 
            v-for="category in categories" 
            :key="category"
            @click="selectedCategory = category"
            :class="['filter-btn', { active: selectedCategory === category }]"
          >
            {{ category }}
          </button>
        </div>
      </div>
      
      <!-- Gallery Grid -->
      <TransitionGroup name="gallery-list" tag="div" class="gallery-grid">
        <div 
          v-for="item in displayItems" 
          :key="item.id" 
          class="gallery-card"
          @click="openModal(item)"
        >
          <ImageSlider 
            class="card-image"
            :image="item.image"
            :images="item.images"
            :icon="item.icon"
            :gradient="item.gradient"
          />
          <div class="card-overlay">
            <div class="overlay-content">
              <span class="view-btn">مشاهده پروژه</span>
            </div>
          </div>
          <div class="card-badge" :style="{ background: item.categoryColor }">{{ item.category }}</div>
          <div class="card-stats">
            <span>❤️ {{ item.likes }}</span>
          </div>
          <div class="card-body">
            <h3 class="card-title">{{ item.title }}</h3>
            <p class="card-description">{{ item.description }}</p>
            <div class="card-tags">
              <span v-for="tag in item.tags.slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
        </div>
      </TransitionGroup>
      
      <!-- Empty State -->
      <div v-if="filteredItems.length === 0" class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>موردی یافت نشد</h3>
        <p>لطفاً فیلتر یا جستجوی دیگری امتحان کنید</p>
      </div>
    </div>
    
    <!-- Enhanced Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedItem" class="modal-overlay" @click="closeModal">
          <div class="modal-content" @click.stop>
            <button class="modal-close" @click="closeModal">✕</button>
            
            <!-- Modal Gallery -->
            <div class="modal-gallery">
              <div class="modal-main-image" :style="{ background: selectedItem.gradient }">
                <div class="modal-icon-large">{{ selectedItem.icon }}</div>
              </div>
              <div class="modal-thumbnails">
                <div 
                  v-for="(img, index) in selectedItem.images" 
                  :key="index"
                  class="thumbnail"
                  :style="{ background: img.gradient }"
                >
                  {{ img.icon }}
                </div>
              </div>
            </div>
            
            <!-- Modal Info -->
            <div class="modal-info">
              <div class="modal-header-row">
                <h2 class="modal-title">{{ selectedItem.title }}</h2>
                <div class="modal-category-badge" :style="{ background: selectedItem.categoryColor }">
                  {{ selectedItem.category }}
                </div>
              </div>
              
              <div class="modal-stats-row">
                <span class="stat-item">👁️ {{ selectedItem.views }} بازدید</span>
                <span class="stat-item">❤️ {{ selectedItem.likes }} لایک</span>
                <span class="stat-item">📅 {{ selectedItem.date }}</span>
              </div>
              
              <p class="modal-description">{{ selectedItem.description }}</p>
              <p class="modal-details">{{ selectedItem.details }}</p>
              
              <div class="modal-features">
                <h3>ویژگی‌های پروژه</h3>
                <ul>
                  <li v-for="feature in selectedItem.features" :key="feature">{{ feature }}</li>
                </ul>
              </div>
              
              <div class="modal-tech">
                <h3>تکنولوژی‌ها</h3>
                <div class="tech-stack">
                  <span v-for="tech in selectedItem.technologies" :key="tech" class="tech-badge">{{ tech }}</span>
                </div>
              </div>
              
              <div class="modal-tags">
                <span v-for="tag in selectedItem.tags" :key="tag" class="tag-large">{{ tag }}</span>
              </div>
              
              <div class="modal-actions">
                <button class="action-btn primary">
                  <span>🔗</span>
                  مشاهده دمو
                </button>
                <button class="action-btn secondary">
                  <span>💬</span>
                  تماس با ما
                </button>
              </div>
            </div>
            
            <div class="modal-navigation">
              <button @click="previousItem" class="nav-btn">
                <span>→</span>
                قبلی
              </button>
              <span class="modal-counter">{{ currentIndex + 1 }} از {{ galleryItems.length }}</span>
              <button @click="nextItem" class="nav-btn">
                بعدی
                <span>←</span>
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import ImageSlider from './ImageSlider.vue'

const props = defineProps({
  showViewAll: {
    type: Boolean,
    default: false
  }
})

const galleryItems = ref([
  {
    id: 1,
    title: 'فروشگاه آنلاین مد و پوشاک',
    description: 'پلتفرم فروش آنلاین با رابط کاربری مدرن و سیستم پرداخت امن',
    details: 'یک فروشگاه آنلاین کامل با قابلیت‌های پیشرفته مدیریت محصولات، سبد خرید هوشمند، سیستم پرداخت امن و پنل مدیریت جامع. این پروژه با تمرکز بر تجربه کاربری و عملکرد بالا طراحی شده است.',
    icon: '🛍️',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    category: 'وب',
    categoryColor: '#667eea',
    views: '۲٫۵ هزار',
    likes: '۱۸۵',
    date: '۱۴۰۴/۱۰/۱۵',
    tags: ['فروشگاه', 'Vue.js', 'Node.js', 'پرداخت آنلاین'],
    technologies: ['Vue 3', 'Node.js', 'MongoDB', 'Stripe', 'Tailwind CSS'],
    features: [
      'سیستم پرداخت آنلاین امن',
      'پنل مدیریت پیشرفته',
      'فیلتر و جستجوی هوشمند',
      'سیستم تخفیف و کوپن',
      'پیگیری سفارش',
      'سیستم نظرات و امتیازدهی'
    ],
    images: [
      { icon: '🏠', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
      { icon: '🛒', gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
      { icon: '💳', gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }
    ]
  },
  {
    id: 2,
    title: 'اپلیکیشن مدیریت پروژه',
    description: 'نرم‌افزار مدیریت پروژه با امکانات تیمی و گزارش‌گیری پیشرفته',
    details: 'یک سیستم جامع مدیریت پروژه برای تیم‌های بزرگ با قابلیت‌های Kanban، Gantt Chart، مدیریت زمان، تخصیص منابع و گزارش‌های تحلیلی پیشرفته. این پلتفرم به تیم‌ها کمک می‌کند تا بهره‌وری خود را تا ۴۰٪ افزایش دهند.',
    icon: '📊',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    category: 'نرم‌افزار',
    categoryColor: '#f093fb',
    views: '۳٫۱ هزار',
    likes: '۲۲۳',
    date: '۱۴۰۴/۰۹/۲۸',
    tags: ['مدیریت پروژه', 'React', 'GraphQL', 'Real-time'],
    technologies: ['React', 'Node.js', 'PostgreSQL', 'Socket.io', 'Redis'],
    features: [
      'داشبورد تحلیلی پیشرفته',
      'مدیریت تسک با Drag & Drop',
      'چت تیمی درون‌برنامه‌ای',
      'تقویم و یادآوری هوشمند',
      'گزارش‌های سفارشی',
      'یکپارچگی با ابزارهای محبوب'
    ],
    images: [
      { icon: '📋', gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
      { icon: '👥', gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' },
      { icon: '📈', gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }
    ]
  },
  {
    id: 3,
    title: 'سیستم رزرو هتل آنلاین',
    description: 'پلتفرم رزرو اتاق هتل با نقشه تعاملی و مقایسه قیمت',
    details: 'یک سیستم رزرو کامل برای هتل‌ها و مسافران با امکانات جستجوی پیشرفته، نقشه‌های تعاملی، مقایسه قیمت، نظرات کاربران و پرداخت امن. این پروژه باعث افزایش ۶۵٪ رزروهای آنلاین شد.',
    icon: '🏨',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    category: 'وب',
    categoryColor: '#4facfe',
    views: '۴٫۸ هزار',
    likes: '۳۵۷',
    date: '۱۴۰۴/۰۹/۱۲',
    tags: ['رزرو آنلاین', 'Next.js', 'Maps API', 'پرداخت'],
    technologies: ['Next.js', 'TypeScript', 'Prisma', 'Stripe', 'Google Maps'],
    features: [
      'جستجوی هوشمند با فیلترهای پیشرفته',
      'نقشه تعاملی موقعیت هتل‌ها',
      'سیستم نظرات و امتیازدهی',
      'مقایسه قیمت‌ها',
      'رزرو لحظه‌ای',
      'پنل مدیریت هتل'
    ],
    images: [
      { icon: '🗺️', gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' },
      { icon: '⭐', gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' },
      { icon: '📱', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }
    ]
  },
  {
    id: 4,
    title: 'اپ موبایل فیتنس و تناسب اندام',
    description: 'اپلیکیشن موبایل برنامه ورزشی شخصی‌سازی شده با AI',
    details: 'اپلیکیشن جامع فیتنس با هوش مصنوعی که برنامه‌های ورزشی شخصی‌سازی شده، ردیابی تغذیه، چالش‌های تیمی و مربی مجازی ارائه می‌دهد. بیش از ۵۰ هزار کاربر فعال در ۶ ماه اول.',
    icon: '💪',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    category: 'موبایل',
    categoryColor: '#43e97b',
    views: '۶٫۲ هزار',
    likes: '۴۵۲',
    date: '۱۴۰۴/۰۸/۲۵',
    tags: ['فیتنس', 'React Native', 'AI', 'سلامت'],
    technologies: ['React Native', 'Python', 'TensorFlow', 'Firebase', 'HealthKit'],
    features: [
      'برنامه ورزشی شخصی‌سازی شده با AI',
      'ردیابی کالری و تغذیه',
      'ویدیوهای آموزشی تمرینات',
      'چالش‌های تیمی',
      'یکپارچگی با دستگاه‌های پوشیدنی',
      'گزارش پیشرفت'
    ],
    images: [
      { icon: '🏃', gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' },
      { icon: '🥗', gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' },
      { icon: '📊', gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }
    ]
  },
  {
    id: 5,
    title: 'پلتفرم یادگیری آنلاین',
    description: 'سیستم LMS کامل با کلاس زنده، آزمون و گواهینامه',
    details: 'یک سیستم مدیریت یادگیری (LMS) پیشرفته با قابلیت برگزاری کلاس‌های زنده، آپلود ویدیو، آزمون‌های آنلاین، سیستم گواهینامه و انجمن گفتگو. بیش از ۱۰۰ مدرس و ۱۰ هزار دانشجو.',
    icon: '🎓',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    category: 'وب',
    categoryColor: '#fa709a',
    views: '۵٫۴ هزار',
    likes: '۳۹۸',
    date: '۱۴۰۴/۰۸/۰۵',
    tags: ['آموزش', 'LMS', 'Webinar', 'Vue.js'],
    technologies: ['Vue 3', 'Laravel', 'MySQL', 'WebRTC', 'AWS'],
    features: [
      'کلاس‌های زنده با ویدیو کنفرانس',
      'آپلود و مدیریت محتوای ویدیویی',
      'سیستم آزمون و نمره‌دهی خودکار',
      'گواهینامه دیجیتال',
      'انجمن و گفتگوی دانشجویان',
      'پنل مالی و گزارشات'
    ],
    images: [
      { icon: '📚', gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' },
      { icon: '🎥', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
      { icon: '📜', gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }
    ]
  },
  {
    id: 6,
    title: 'داشبورد تحلیل داده',
    description: 'پنل تحلیلی داده با نمودارهای تعاملی و گزارش‌های لحظه‌ای',
    details: 'یک داشبورد تحلیلی قدرتمند برای تجزیه و تحلیل داده‌های کسب‌وکار با نمودارهای تعاملی، فیلترهای پیشرفته، گزارش‌های سفارشی و پیش‌بینی روندها با یادگیری ماشین.',
    icon: '📈',
    gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    category: 'نرم‌افزار',
    categoryColor: '#30cfd0',
    views: '۳٫۷ هزار',
    likes: '۲۸۹',
    date: '۱۴۰۴/۰۷/۲۰',
    tags: ['Analytics', 'Data Viz', 'Dashboard', 'React'],
    technologies: ['React', 'D3.js', 'Python', 'FastAPI', 'PostgreSQL'],
    features: [
      'نمودارهای تعاملی با D3.js',
      'فیلترهای پیشرفته و پویا',
      'گزارش‌های سفارشی PDF/Excel',
      'پیش‌بینی روندها با ML',
      'Real-time data updates',
      'API برای یکپارچگی'
    ],
    images: [
      { icon: '📊', gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)' },
      { icon: '📉', gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
      { icon: '🎯', gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }
    ]
  },
  {
    id: 7,
    title: 'سیستم مدیریت رستوران',
    description: 'نرم‌افزار POS و مدیریت رستوران با منوی دیجیتال',
    details: 'سیستم کامل مدیریت رستوران شامل POS، مدیریت میز، سفارش آنلاین، منوی دیجیتال، مدیریت انبار و حسابداری. این سیستم سرعت سرویس‌دهی را ۵۰٪ افزایش داد.',
    icon: '🍽️',
    gradient: 'linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)',
    category: 'نرم‌افزار',
    categoryColor: '#ff6b6b',
    views: '۲٫۹ هزار',
    likes: '۱۹۵',
    date: '۱۴۰۴/۰۷/۰۸',
    tags: ['رستوران', 'POS', 'سفارش آنلاین', 'Electron'],
    technologies: ['Electron', 'Vue.js', 'Node.js', 'SQLite', 'Printer API'],
    features: [
      'سیستم POS پیشرفته',
      'مدیریت میز و رزرو',
      'منوی دیجیتال با QR Code',
      'سفارش آنلاین',
      'مدیریت انبار و موجودی',
      'گزارش‌های مالی'
    ],
    images: [
      { icon: '🍕', gradient: 'linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)' },
      { icon: '💳', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
      { icon: '📱', gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }
    ]
  },
  {
    id: 8,
    title: 'شبکه اجتماعی عکاسان',
    description: 'پلتفرم اشتراک‌گذاری عکس با قابلیت فروش و مجوز',
    details: 'یک شبکه اجتماعی تخصصی برای عکاسان با امکان آپلود پرتفولیو، فروش عکس، سیستم مجوزدهی، جامعه عکاسان و مسابقات ماهانه. بیش از ۲۰ هزار عکاس عضو.',
    icon: '📷',
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    category: 'وب',
    categoryColor: '#a8edea',
    views: '۷٫۱ هزار',
    likes: '۵۶۸',
    date: '۱۴۰۴/۰۶/۱۵',
    tags: ['شبکه اجتماعی', 'عکاسی', 'فروش', 'Next.js'],
    technologies: ['Next.js', 'Cloudinary', 'Stripe', 'PostgreSQL', 'Redis'],
    features: [
      'گالری پرتفولیوی حرفه‌ای',
      'فروش عکس با سیستم مجوز',
      'فید اجتماعی و دنبال‌کنندگان',
      'مسابقات و جوایز',
      'ویرایشگر آنلاین عکس',
      'تحلیل آمار و فروش'
    ],
    images: [
      { icon: '🖼️', gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)' },
      { icon: '💰', gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' },
      { icon: '🏆', gradient: 'linear-gradient(135deg, #feca57 0%, #ff6b6b 100%)' }
    ]
  },
  {
    id: 9,
    title: 'اپلیکیشن تاکسی آنلاین',
    description: 'پلتفرم درخواست تاکسی با نقشه لحظه‌ای و پرداخت آنلاین',
    details: 'یک اپلیکیشن کامل درخواست تاکسی شامل نقشه‌های زنده، ردیابی مسیر، محاسبه هوشمند قیمت، پرداخت آنلاین، امتیازدهی و چت با راننده. بیش از ۱۵ هزار سفر روزانه.',
    icon: '🚕',
    gradient: 'linear-gradient(135deg, #ffd89b 0%, #19547b 100%)',
    category: 'موبایل',
    categoryColor: '#ffd89b',
    views: '۸٫۵ هزار',
    likes: '۶۲۳',
    date: '۱۴۰۴/۰۵/۲۸',
    tags: ['تاکسی', 'نقشه', 'GPS', 'Flutter'],
    technologies: ['Flutter', 'Node.js', 'Socket.io', 'Google Maps', 'Firebase'],
    features: [
      'نقشه زنده و ردیابی مسیر',
      'محاسبه هوشمند قیمت',
      'پرداخت آنلاین چندگانه',
      'چت با راننده',
      'سیستم امتیازدهی',
      'تخمین زمان رسیدن'
    ],
    images: [
      { icon: '🗺️', gradient: 'linear-gradient(135deg, #ffd89b 0%, #19547b 100%)' },
      { icon: '🚗', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
      { icon: '💳', gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' }
    ]
  }
])

const selectedItem = ref(null)
const searchQuery = ref('')
const selectedCategory = ref('همه')

const categories = computed(() => {
  const cats = ['همه', ...new Set(galleryItems.value.map(item => item.category))]
  return cats
})

const filteredItems = computed(() => {
  let items = galleryItems.value

  // Filter by category
  if (selectedCategory.value !== 'همه') {
    items = items.filter(item => item.category === selectedCategory.value)
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    items = items.filter(item => 
      item.title.toLowerCase().includes(query) ||
      item.description.toLowerCase().includes(query) ||
      item.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }

  return items
})

const displayItems = computed(() => {
  return props.showViewAll ? filteredItems.value.slice(0, 6) : filteredItems.value
})

const currentIndex = computed(() => 
  selectedItem.value ? galleryItems.value.findIndex(item => item.id === selectedItem.value.id) : 0
)

const openModal = (item) => {
  selectedItem.value = item
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  selectedItem.value = null
  document.body.style.overflow = ''
}

const nextItem = () => {
  const nextIndex = (currentIndex.value + 1) % galleryItems.value.length
  selectedItem.value = galleryItems.value[nextIndex]
}

const previousItem = () => {
  const prevIndex = (currentIndex.value - 1 + galleryItems.value.length) % galleryItems.value.length
  selectedItem.value = galleryItems.value[prevIndex]
}
</script>

<style scoped>
.gallery-section {
  padding: 6rem 0;
  background: rgba(248, 249, 250, 0.5);
  position: relative;
}

.dark-mode .gallery-section {
  background: rgba(45, 45, 45, 0.3);
}

/* Controls */
.gallery-controls {
  display: flex;
  gap: 2rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  flex: 1;
  min-width: 280px;
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  right: 1.5rem;
  font-size: 1.2rem;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 1rem 3.5rem 1rem 1.5rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  color: #1a1a1a;
}

.dark-mode .search-input {
  background: rgba(45, 45, 45, 0.8);
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.1);
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.filter-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  background: white;
  color: #1a1a1a;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.dark-mode .filter-btn {
  background: rgba(45, 45, 45, 0.8);
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.1);
}

.filter-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.filter-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 5rem 2rem;
  color: #6c757d;
}

.dark-mode .empty-state {
  color: #a0a0a0;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #1a1a1a;
}

.dark-mode .empty-state h3 {
  color: #ffffff;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
  position: relative;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.dark-mode .section-title {
  color: #ffffff;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.dark-mode .section-subtitle {
  color: #a0a0a0;
}

.view-all-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.view-all-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-icon {
  transition: transform 0.3s ease;
}

.view-all-btn:hover .btn-icon {
  transform: translateX(5px);
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.gallery-card {
  background: white;
  border-radius: 20px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.dark-mode .gallery-card {
  background: rgba(45, 45, 45, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

.gallery-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.dark-mode .gallery-card:hover {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.card-image {
  height: 280px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon-main {
  font-size: 6rem;
  z-index: 1;
  position: relative;
  filter: drop-shadow(0 8px 20px rgba(0, 0, 0, 0.3));
  transition: all 0.4s ease;
  opacity: 1;
}

.gallery-card:hover .card-icon-main {
  transform: scale(1.15) rotate(5deg);
  filter: drop-shadow(0 12px 30px rgba(0, 0, 0, 0.4));
  opacity: 0.2;
}

.card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(0px);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s ease;
  z-index: 2;
}

.gallery-card:hover .card-overlay {
  opacity: 1;
  backdrop-filter: blur(5px);
}

.overlay-content {
  position: absolute;
  text-align: center;
}

.view-btn {
  background: white;
  color: #1a1a1a;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-weight: 700;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  display: inline-block;
}

.card-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.card-stats {
  position: absolute;
  bottom: 1rem;
  left: 1rem;
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
}

.card-stats span {
  background: rgba(255, 255, 255, 0.95);
  padding: 0.4rem 0.8rem;
  border-radius: 50px;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.card-body {
  padding: 2rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #1a1a1a;
  line-height: 1.4;
}

.dark-mode .card-title {
  color: #ffffff;
}

.card-description {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #6c757d;
  margin-bottom: 1rem;
  flex: 1;
}

.dark-mode .card-description {
  color: #a0a0a0;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: auto;
}

.tag {
  padding: 0.4rem 0.8rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 50px;
  font-size: 0.8rem;
  color: #667eea;
  font-weight: 500;
}

/* Transition */
.gallery-list-move,
.gallery-list-enter-active,
.gallery-list-leave-active {
  transition: all 0.5s ease;
}

.gallery-list-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(30px);
}

.gallery-list-leave-to {
  opacity: 0;
  transform: scale(0.8) translateY(-30px);
}

.gallery-list-leave-active {
  position: absolute;
}

/* Enhanced Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.90);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 2rem;
  overflow-y: auto;
}

.modal-content {
  background: white;
  border-radius: 30px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
}

.dark-mode .modal-content {
  background: #2d2d2d;
}

.modal-gallery {
  position: relative;
}

.modal-main-image {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 30px 30px 0 0;
  position: relative;
}

.modal-icon-large {
  font-size: 8rem;
}

.modal-thumbnails {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.75rem;
}

.thumbnail {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  border: 3px solid white;
}

.thumbnail:hover {
  transform: translateY(-5px);
}

.modal-info {
  padding: 2.5rem;
}

.modal-close {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: #1a1a1a;
  z-index: 10;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.dark-mode .modal-close {
  background: rgba(45, 45, 45, 0.95);
  color: #ffffff;
}

.modal-close:hover {
  background: #ff0000;
  color: white;
  transform: scale(1.1) rotate(90deg);
}

.modal-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.modal-category-badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  white-space: nowrap;
}

.modal-stats-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.stat-item {
  color: #6c757d;
  font-size: 0.95rem;
  font-weight: 500;
}

.dark-mode .stat-item {
  color: #a0a0a0;
}

.modal-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #1a1a1a;
  line-height: 1.3;
  flex: 1;
}

.dark-mode .modal-title {
  color: #ffffff;
}

.modal-description {
  font-size: 1.15rem;
  color: #6c757d;
  margin-bottom: 1.5rem;
  font-weight: 500;
  line-height: 1.7;
}

.dark-mode .modal-description {
  color: #a0a0a0;
}

.modal-details {
  font-size: 1rem;
  line-height: 1.8;
  color: #6c757d;
  text-align: justify;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 15px;
  border-right: 4px solid #667eea;
}

.dark-mode .modal-details {
  color: #a0a0a0;
  background: rgba(102, 126, 234, 0.1);
}

.modal-features {
  margin-bottom: 2rem;
}

.modal-features h3,
.modal-tech h3 {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.dark-mode .modal-features h3,
.dark-mode .modal-tech h3 {
  color: #ffffff;
}

.modal-features ul {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.75rem;
}

.modal-features li {
  padding: 0.75rem 1rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 10px;
  color: #1a1a1a;
  position: relative;
  padding-right: 2rem;
}

.dark-mode .modal-features li {
  background: rgba(102, 126, 234, 0.1);
  color: #ffffff;
}

.modal-features li::before {
  content: '✓';
  position: absolute;
  right: 0.75rem;
  color: #667eea;
  font-weight: 700;
}

.modal-tech {
  margin-bottom: 2rem;
}

.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tech-badge {
  padding: 0.6rem 1.2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.modal-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.tag-large {
  padding: 0.6rem 1.2rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 50px;
  font-size: 0.9rem;
  color: #667eea;
  font-weight: 600;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  padding-top: 2rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.dark-mode .modal-actions {
  border-top-color: rgba(255, 255, 255, 0.1);
}

.action-btn {
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-width: 150px;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.action-btn.secondary {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 2px solid rgba(102, 126, 234, 0.3);
}

.action-btn.secondary:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
}

.modal-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.dark-mode .modal-navigation {
  border-top-color: rgba(255, 255, 255, 0.1);
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.modal-counter {
  font-size: 0.9rem;
  color: #6c757d;
  font-weight: 500;
}

.dark-mode .modal-counter {
  color: #a0a0a0;
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9);
}

@media (max-width: 768px) {
  .gallery-section {
    padding: 4rem 0;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .gallery-controls {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-box {
    min-width: 100%;
  }
  
  .filter-buttons {
    width: 100%;
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 0.5rem;
  }
  
  .gallery-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .card-image {
    height: 220px;
  }
  
  .card-icon-main {
    font-size: 4rem;
  }
  
  .modal-overlay {
    padding: 1rem;
  }
  
  .modal-content {
    border-radius: 20px;
  }
  
  .modal-main-image {
    height: 250px;
    border-radius: 20px 20px 0 0;
  }
  
  .modal-icon-large {
    font-size: 5rem;
  }
  
  .modal-info {
    padding: 1.5rem;
  }
  
  .modal-title {
    font-size: 1.5rem;
  }
  
  .modal-features ul {
    grid-template-columns: 1fr;
  }
  
  .modal-navigation {
    flex-direction: column;
    gap: 1rem;
    padding: 1.5rem;
  }
  
  .nav-btn {
    width: 100%;
    justify-content: center;
  }
  
  .modal-counter {
    order: -1;
  }
  
  .action-btn {
    min-width: 100%;
  }
}

@media (max-width: 480px) {
  .modal-header-row {
    flex-direction: column;
  }
  
  .modal-stats-row {
    flex-direction: column;
    gap: 0.75rem;
  }
}
</style>
