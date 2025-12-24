# پیاده‌سازی بخش‌های پروژه‌ها و مقالات

## خلاصه کار انجام‌شده

تمام اجزاء لازم برای اضافه کردن بخش‌های پروژه‌ها و مقالات به سیستم BIM پیاده‌سازی شده است.

---

## فاز ۱: بخش پروژه‌ها در صفحه‌ی اصلی ✅

### تغییرات Backend

#### ۱. مدل Project در [app/models/models.py](backend/app/models/models.py)
```python
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String(255), nullable=False, index=True)
    title_fa = Column(String(255), nullable=True)
    description_en = Column(Text, nullable=False)
    description_fa = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    archive_url = Column(String(500), nullable=True)
    iframe_url = Column(String(500), nullable=True)
    category = Column(String(50), nullable=True, index=True)
    order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**فیلدهای کلیدی:**
- `title_en/fa`: عنوان دو‌زبانه
- `description_en/fa`: توضیحات دو‌زبانه
- `image_url`: تصویر شاخص پروژه
- `archive_url`: لینک دانلود آرشیو (اختیاری)
- `iframe_url`: URL برای نمایش iframe (اختیاری)
- `category`: دسته‌بندی (BIM/Surveying)
- `order`: ترتیب نمایش
- `is_featured`: پروژه‌های برجسته

#### ۲. API Endpoints در [app/routers/projects.py](backend/app/routers/projects.py)

```
GET /api/projects                    - لیست تمام پروژه‌ها (با فیلتر category و featured)
GET /api/projects/{project_id}       - جزئیات یک پروژه
POST /api/projects                   - ایجاد پروژه (فقط Admin)
PUT /api/projects/{project_id}       - به‌روزرسانی پروژه (فقط Admin)
DELETE /api/projects/{project_id}    - حذف پروژه (فقط Admin)
```

**Query Parameters:**
```
GET /api/projects?category=BIM&featured=true
```

#### ۳. Schemas در [app/schemas/schemas.py](backend/app/schemas/schemas.py)
- `ProjectCreate`: برای ایجاد پروژه جدید
- `ProjectUpdate`: برای به‌روزرسانی پروژه
- `ProjectResponse`: برای پاسخ API

#### ۴. Cache Keys در [app/cache.py](backend/app/cache.py)
```python
"projects": "cache:projects"
"projects": 3600  # TTL: 1 ساعت
```

#### ۵. Router Registration در [main.py](backend/main.py)
```python
from app.routers import projects, articles
app.include_router(projects.router, prefix="/api")
app.include_router(articles.router, prefix="/api")
```

### تغییرات Frontend

#### ۱. کامپوننت [Projects.vue](src/components/Projects.vue)
- **موقعیت:** بعد از BimServices، قبل از SurveyingServices
- **Layout:** شبکه ۳ ستونی (responsive: ۲ ستون @ 1024px، ۱ ستون @ 768px)
- **انیمیشن‌ها:** `animate-on-scroll` با staggered delays
- **Features:**
  - نمایش ۶ پروژه نمونه
  - لینک به جزئیات پروژه
  - دکمه دانلود آرشیو (اختیاری)

#### ۲. به‌روزرسانی [App.vue](src/App.vue)
- اضافه کردن import برای `Projects.vue`
- اضافه کردن component به template
- ثبت component در `components` object

#### ۳. به‌روزرسانی [Header.vue](src/components/Header.vue)
- اضافه کردن لینک "پروژه‌ها" به navigation
- لینک هدایت به صفحه آرشیو پروژه‌ها: `#projects-archive`

---

## فاز ۲: صفحات مقالات و آرشیو ✅

### تغییرات Backend

#### ۱. مدل Article در [app/models/models.py](backend/app/models/models.py)
```python
class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String(255), nullable=False, index=True)
    title_fa = Column(String(255), nullable=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    summary_en = Column(Text, nullable=False)
    summary_fa = Column(Text, nullable=True)
    content_en = Column(Text, nullable=False)
    content_fa = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    tags = Column(String(500), nullable=True)  # Comma-separated
    category = Column(String(100), nullable=True, index=True)
    author = Column(String(255), nullable=True)
    is_published = Column(Boolean, default=True, index=True)
    publish_date = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**فیلدهای کلیدی:**
- `slug`: URL-friendly شناخت مقاله
- `summary_en/fa`: خلاصه مقاله
- `content_en/fa`: متن کامل مقاله
- `tags`: تگ‌های جستجو (comma-separated)
- `is_published`: منتشر‌شده یا پیش‌نویس
- `publish_date`: تاریخ انتشار

#### ۲. API Endpoints در [app/routers/articles.py](backend/app/routers/articles.py)

```
GET /api/articles                           - لیست مقالات منتشرشده (pagination)
GET /api/articles/{article_id_or_slug}      - جزئیات یک مقاله (by ID or slug)
GET /api/articles/tags/all                  - لیست تمام تگ‌های موجود
POST /api/articles                          - ایجاد مقاله (فقط Admin)
PUT /api/articles/{article_id}              - به‌روزرسانی مقاله (فقط Admin)
DELETE /api/articles/{article_id}           - حذف مقاله (فقط Admin)
```

**Query Parameters:**
```
GET /api/articles?skip=0&limit=10&tag=BIM&category=News
```

#### ۳. Schemas در [app/schemas/schemas.py](backend/app/schemas/schemas.py)
- `ArticleCreate`: برای ایجاد مقاله
- `ArticleUpdate`: برای به‌روزرسانی مقاله
- `ArticleResponse`: برای پاسخ API

#### ۴. Cache Keys در [app/cache.py](backend/app/cache.py)
```python
"articles": "cache:articles"
"articles": 1800  # TTL: ۳۰ دقیقه
```

### تغییرات Frontend

#### ۱. کامپوننت [ArticlesArchive.vue](src/components/ArticlesArchive.vue)
- **صفحه:** آرشیو تمام مقالات
- **Route:** `#articles`
- **Features:**
  - لیست مقالات با تصویر و خلاصه
  - فیلتر بر اساس دسته‌بندی
  - جستجو در عنوان و متن
  - Pagination (۶ مقاله در هر صفحه)
  - نمایش تگ‌ها
  - لینک مطالعه بیشتر

#### ۲. کامپوننت [ArticleDetail.vue](src/components/ArticleDetail.vue)
- **صفحه:** جزئیات یک مقاله
- **Route:** `#article/{slug_or_id}`
- **Features:**
  - متادیتا (دسته‌بندی، نویسنده، تاریخ)
  - تصویر شاخص (full-width)
  - محتوای کامل مقاله (HTML support)
  - تگ‌های مقاله
  - دکمه‌های اشتراک‌گذاری (Twitter, Facebook, LinkedIn, Copy Link)
  - پیشنهاد مقالات مرتبط

#### ۳. به‌روزرسانی [Header.vue](src/components/Header.vue)
- اضافه کردن لینک "مقالات" به navigation
- لینک هدایت به آرشیو مقالات: `#articles`

---

## فاز ۳: صفحات پروژه‌ها و جزئیات ✅

### تغییرات Frontend

#### ۱. کامپوننت [ProjectsArchive.vue](src/components/ProjectsArchive.vue)
- **صفحه:** آرشیو تمام پروژه‌ها
- **Route:** `#projects-archive`
- **Features:**
  - شبکه ۳ ستونی با overlay
  - فیلتر بر اساس دسته‌بندی
  - نمایش دسته‌بندی روی کارت
  - دکمه "مشاهده پروژه" در overlay
  - Responsive design

#### ۲. کامپوننت [ProjectDetail.vue](src/components/ProjectDetail.vue)
- **صفحه:** جزئیات یک پروژه
- **Route:** `#project/{project_id}`
- **SEO Elements:**
  - عنوان بزرگ و مناسب
  - متادیتای ساختارمند (JSON-LD)
  - Canonical URLs

**Sections:**
1. **تصویر شاخص** (full-width, 500px height)
2. **iframe Section** (اگر `iframe_url` موجود باشد)
   - Height: 600px
   - Full-width
   - Support for fullscreen
3. **بخش توضیحات**
   - عنوان: "درباره‌ی پروژه"
   - متن توضیحی
   - دکمه دانلود آرشیو (اختیاری)
4. **جدول جزئیات**
   - نوع پروژه
   - تاریخ ایجاد
   - آخرین بروزرسانی
5. **Call to Action**
   - متن: "آیا برای پروژه شما هم نیاز به خدمات مشابه دارید؟"
   - دکمه: "تماس با ما" → `#contact`
6. **پروژه‌های مرتبط** (۳ پروژه از همان دسته‌بندی)

### تغییرات Frontend - Routing

#### بروزرسانی [App.vue](src/App.vue)
```javascript
// Routing Logic:
- #home                    → Home Page
- #articles                → Articles Archive
- #article/{slug_or_id}    → Article Detail
- #projects-archive        → Projects Archive
- #project/{id}            → Project Detail
- (default/other hashes)   → Home Page
```

**Components:**
- Import تمام 4 کامپوننت جدید
- Dynamic rendering based on `currentPage` state
- Hash change listener
- Automatic animation re-initialization

---

## ساختار دایرکتوری تغییریافته

```
backend/
  app/
    models/
      models.py              ← +Project, +Article
    routers/
      projects.py            ← (جدید)
      articles.py            ← (جدید)
    schemas/
      schemas.py             ← +ProjectResponse, +ArticleResponse
    cache.py                 ← +projects, +articles cache keys

src/
  components/
    Projects.vue             ← (جدید)
    ProjectsArchive.vue      ← (جدید)
    ProjectDetail.vue        ← (جدید)
    ArticlesArchive.vue      ← (جدید)
    ArticleDetail.vue        ← (جدید)
    Header.vue               ← (به‌روزرسانی: +2 لینک navigation)
    App.vue                  ← (به‌روزرسانی: routing logic)
```

---

## راهنمای استفاده

### ۱. صفحه اصلی - بخش پروژه‌ها
- موقعیت: بعد از خدمات BIM
- لینک: `#projects-archive`
- کارت‌های نمونه: ۶ پروژه

### ۲. صفحه آرشیو پروژه‌ها
```
URL: yoursite.com/#projects-archive
Features:
  - فیلتر بر اساس دسته‌بندی
  - ۹ پروژه با pagination (اختیاری)
  - Overlay effect
```

### ۳. صفحه جزئیات پروژه
```
URL: yoursite.com/#project/1
Content:
  - تصویر شاخص
  - iframe (اگر موجود باشد)
  - توضیحات
  - اطلاعات پروژه
  - پروژه‌های مرتبط
```

### ۴. صفحه آرشیو مقالات
```
URL: yoursite.com/#articles
Features:
  - لیستی با پیکربندی
  - فیلتر: دسته‌بندی، جستجو
  - Pagination: ۶ مقاله در صفحه
  - نمایش تگ‌ها
```

### ۵. صفحه جزئیات مقاله
```
URL: yoursite.com/#article/bim-benefits-2024
Content:
  - متادیتا (نویسنده، تاریخ، دسته‌بندی)
  - تصویر شاخص
  - خلاصه
  - متن کامل (HTML support)
  - تگ‌های مقاله
  - دکمه‌های اشتراک‌گذاری
  - مقالات مرتبط
```

---

## نکات مهم

### Design & Styling
✅ استفاده از ساختار موجود  
✅ بدون Shadow غیرضروری  
✅ بدون Gradient  
✅ Border‌های ظریف و محدود  
✅ Borders: `1px solid #e8e8e8`  
✅ استفاده از رنگ اصلی: `#1abc9c`  
✅ انیمیشن‌های GPU-accelerated  
✅ Staggered animations با delays

### Responsive Design
✅ Desktop: 3 ستون → ۱۲۰۰px max-width  
✅ Tablet (1024px): 2 ستون  
✅ Mobile (768px): 1 ستون  
✅ Small Mobile (480px): Optimized layout

### RTL Support
✅ `direction: rtl` global  
✅ `text-align: right` default  
✅ Flexbox: `flex-direction` properly configured  
✅ Position offsets: `right` instead of `left`

### SEO Considerations
- Semantic HTML tags (`<section>`, `<article>`, `<h1>`, etc.)
- Proper heading hierarchy
- Meta descriptions (prepared for implementation)
- JSON-LD structured data (template ready)
- Open Graph tags (template ready)
- Slug-based URLs for articles
- Canonical URLs support

---

## مراحل بعدی (پیشنهادی)

### ۱. API Integration
```javascript
// Create api.js service
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
})
```

### ۲. Database Migrations
```bash
# Create migration files for new tables
alembic revision --autogenerate -m "Add Project and Article models"
alembic upgrade head
```

### ۳. Admin Panel Integration
- Dashboard برای مدیریت پروژه‌ها
- Dashboard برای مدیریت مقالات
- Upload images interface
- Rich text editor برای مقالات

### ۴. SEO Meta Tags
```javascript
// Update page title and meta based on route
window.document.title = `${article.title_fa} - GeoBiro`
```

### ۵. Analytics
- Track page views
- Track article reads
- Track project views

---

## فایل‌های تغییریافته

### Backend
1. ✅ [app/models/models.py](backend/app/models/models.py) - +2 مدل
2. ✅ [app/routers/projects.py](backend/app/routers/projects.py) - (جدید)
3. ✅ [app/routers/articles.py](backend/app/routers/articles.py) - (جدید)
4. ✅ [app/schemas/schemas.py](backend/app/schemas/schemas.py) - +4 schema
5. ✅ [app/cache.py](backend/app/cache.py) - +2 cache key
6. ✅ [main.py](backend/main.py) - Router registration

### Frontend
1. ✅ [src/App.vue](src/App.vue) - Routing system
2. ✅ [src/components/Header.vue](src/components/Header.vue) - +2 nav links
3. ✅ [src/components/Projects.vue](src/components/Projects.vue) - (جدید)
4. ✅ [src/components/ProjectsArchive.vue](src/components/ProjectsArchive.vue) - (جدید)
5. ✅ [src/components/ProjectDetail.vue](src/components/ProjectDetail.vue) - (جدید)
6. ✅ [src/components/ArticlesArchive.vue](src/components/ArticlesArchive.vue) - (جدید)
7. ✅ [src/components/ArticleDetail.vue](src/components/ArticleDetail.vue) - (جدید)

---

## نسخه

- **Version:** 1.0.0
- **Date:** 25 دسامبر ۲۰۲۵
- **Status:** ✅ Complete - Ready for Testing

---

## نکات نهایی

تمام کامپوننت‌ها با **نمونه‌ داده sample data** پیاده‌سازی شده‌اند. برای استفاده واقعی، باید API calls یا state management راه‌اندازی شود. کامپوننت‌ها آماده برای integration با بخش backend API هستند.

