# Quick Reference Guide - پروژه‌ها و مقالات

## 🔗 API Routes

### Projects API
```
GET    /api/projects                    List all projects
GET    /api/projects?category=BIM       Filter by category
GET    /api/projects?featured=true      Get featured projects
GET    /api/projects/{id}               Get project details
POST   /api/projects                    Create project (Admin)
PUT    /api/projects/{id}               Update project (Admin)
DELETE /api/projects/{id}               Delete project (Admin)
```

### Articles API
```
GET    /api/articles                    List articles (paginated)
GET    /api/articles?skip=0&limit=10    Pagination
GET    /api/articles?tag=BIM            Filter by tag
GET    /api/articles?category=News      Filter by category
GET    /api/articles/{id_or_slug}       Get article details
GET    /api/articles/tags/all           Get all tags
POST   /api/articles                    Create article (Admin)
PUT    /api/articles/{id}               Update article (Admin)
DELETE /api/articles/{id}               Delete article (Admin)
```

---

## 🧩 Frontend Routes (Hash-based)

### Home & Main Pages
```
#home                   Home page (default)
#bim                    Jump to BIM services
#surveying              Jump to surveying services
#projects               Projects section (home page)
#about                  Jump to about section
#contact                Jump to contact section
```

### Projects
```
#projects-archive       Projects archive page
#project/1              Project detail (by ID)
#project/2              Another project
```

### Articles
```
#articles               Articles archive page
#article/slug-name      Article detail (by slug)
#article/1              Article detail (by ID)
```

**Examples:**
```
yoursite.com/#articles
yoursite.com/#article/bim-benefits-2024
yoursite.com/#projects-archive
yoursite.com/#project/3
```

---

## 📦 Component Props & Data

### Projects.vue
```vue
<template>
  <!-- Shows 6 featured projects on home page -->
</template>

<script>
data() {
  return {
    projects: [],        // Project objects array
    loading: false,      // Loading state
    error: null         // Error message
  }
}
</script>
```

**Props:** None (fetches own data)

### ProjectsArchive.vue
```vue
<template>
  <!-- Shows all projects with filtering -->
</template>

<script>
data() {
  return {
    projects: [],              // All projects
    filteredProjects: [],      // Filtered result
    selectedCategory: '',      // Filter state
    loading: false,
    error: null
  }
}
</script>
```

**Features:**
- Category filter dropdown
- Grid responsive layout
- Overlay with "View Project" button

### ProjectDetail.vue
```vue
<template>
  <!-- Shows single project with full details -->
</template>

<script>
data() {
  return {
    project: null,           // Current project
    projectId: null,         // From URL
    relatedProjects: [],     // Same category projects
    loading: false,
    error: null
  }
}
</script>
```

**Features:**
- Featured image (full-width)
- iframe section (if iframe_url exists)
- Description section
- Project details grid
- Related projects (3 items)
- Download archive button
- Contact CTA

### ArticlesArchive.vue
```vue
<template>
  <!-- Shows all articles with filtering and pagination -->
</template>

<script>
data() {
  return {
    articles: [],              // All articles
    filteredArticles: [],      // Current page
    currentPage: 1,
    itemsPerPage: 6,
    selectedCategory: '',      // Filter
    searchQuery: '',           // Search
    totalPages: 1,
    loading: false,
    error: null
  }
}
</script>
```

**Features:**
- Category filter
- Text search
- Pagination (6 per page)
- Show tags
- Article summary + image

### ArticleDetail.vue
```vue
<template>
  <!-- Shows full article content -->
</template>

<script>
data() {
  return {
    article: null,           // Current article
    articles: [],            // For sample data
    relatedArticles: [],     // Same category
    loading: false,
    error: null,
    articleId: null         // From URL (slug or ID)
  }
}
</script>
```

**Features:**
- Meta info (author, date, category)
- Featured image (full-width)
- Summary section
- Full content (HTML support)
- Tags display
- Social share buttons (Twitter, Facebook, LinkedIn, Copy)
- Related articles (3 items)

---

## 🎯 Sample Data Structure

### Project Object
```json
{
  "id": 1,
  "title_en": "BIM Modeling Project",
  "title_fa": "پروژه مدل‌سازی BIM",
  "description_en": "A comprehensive 3D BIM model...",
  "description_fa": "یک مدل BIM سه‌بعدی جامع...",
  "image_url": "https://example.com/image.jpg",
  "archive_url": "https://example.com/archive.zip",
  "iframe_url": "https://viewer.example.com/project/1",
  "category": "BIM",
  "order": 1,
  "is_featured": true,
  "created_at": "2024-06-15T10:00:00",
  "updated_at": "2024-12-15T10:00:00"
}
```

### Article Object
```json
{
  "id": 1,
  "slug": "bim-benefits-2024",
  "title_en": "Benefits of BIM Technology",
  "title_fa": "فوایدی فناوری BIM",
  "summary_en": "Explore how BIM is revolutionizing...",
  "summary_fa": "کاوش کنید که چگونه BIM...",
  "content_en": "<h2>What is BIM?</h2><p>Building...</p>",
  "content_fa": "<h2>BIM چیست؟</h2><p>مدل‌سازی...</p>",
  "image_url": "https://example.com/article.jpg",
  "tags": "BIM, Construction, Technology",
  "category": "BIM",
  "author": "GeoBiro Team",
  "is_published": true,
  "publish_date": "2025-01-15T10:00:00",
  "created_at": "2025-01-15T10:00:00",
  "updated_at": "2025-01-15T10:00:00"
}
```

---

## 🎨 CSS Classes & Animations

### Standard Classes
```css
.animate-on-scroll          /* Elements animated on scroll */
.in-view                    /* Applied when element is visible */
.section-title              /* Section heading style */
.container                  /* Content container (max-width: 1200px) */
.btn-primary                /* Primary button style */
.btn-link                   /* Link button style */
.category                   /* Category badge */
.tag                        /* Tag badge */
```

### Animation Names
```css
@keyframes slideUp          /* Slide up animation (12px offset) */
@keyframes fadeIn           /* Fade in animation */
@keyframes scalePulse       /* Scale pulse animation */
@keyframes subtleBounce     /* Subtle bounce animation */
```

### Responsive Prefixes
```css
@media (max-width: 1024px)  /* Tablet */
@media (max-width: 768px)   /* Mobile */
@media (max-width: 480px)   /* Small mobile */
```

---

## 🔄 Navigation Flow

```
Home Page
  ├── Projects Section (Projects.vue)
  │   └── "View Project" → #project/id → ProjectDetail.vue
  ├── "Projects Archive" link → #projects-archive → ProjectsArchive.vue
  │   └── "View Project" → #project/id → ProjectDetail.vue
  ├── "Articles" link → #articles → ArticlesArchive.vue
  │   └── "Read More" → #article/slug → ArticleDetail.vue
  │       └── "Related Articles" → #article/slug → ArticleDetail.vue
  └── Contact section → Contact form
```

---

## 💾 Database Schema

### projects table
```sql
CREATE TABLE projects (
  id                INTEGER PRIMARY KEY,
  title_en         VARCHAR(255) NOT NULL,
  title_fa         VARCHAR(255),
  description_en   TEXT NOT NULL,
  description_fa   TEXT,
  image_url        VARCHAR(500),
  archive_url      VARCHAR(500),
  iframe_url       VARCHAR(500),
  category         VARCHAR(50),
  order            INTEGER DEFAULT 0,
  is_featured      BOOLEAN DEFAULT FALSE,
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### articles table
```sql
CREATE TABLE articles (
  id              INTEGER PRIMARY KEY,
  title_en        VARCHAR(255) NOT NULL,
  title_fa        VARCHAR(255),
  slug            VARCHAR(255) UNIQUE NOT NULL,
  summary_en      TEXT NOT NULL,
  summary_fa      TEXT,
  content_en      TEXT NOT NULL,
  content_fa      TEXT,
  image_url       VARCHAR(500),
  tags            VARCHAR(500),
  category        VARCHAR(100),
  author          VARCHAR(255),
  is_published    BOOLEAN DEFAULT TRUE,
  publish_date    DATETIME DEFAULT CURRENT_TIMESTAMP,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Authentication & Permissions

### API Authentication
```bash
# Register admin user
POST /api/auth/register

# Login
POST /api/auth/login
# Returns: { "access_token": "...", "token_type": "bearer", "user": {...} }

# Use token in headers
Authorization: Bearer {access_token}
```

### Admin-Only Endpoints
```
POST   /api/projects         Create project
PUT    /api/projects/{id}    Update project
DELETE /api/projects/{id}    Delete project
POST   /api/articles         Create article
PUT    /api/articles/{id}    Update article
DELETE /api/articles/{id}    Delete article
```

---

## 🚀 Performance Optimization

### Caching Strategy
```python
# Projects cache (1 hour)
GET /api/projects → cached for 3600s

# Articles cache (30 minutes)
GET /api/articles → cached for 1800s
# Cache invalidated on POST/PUT/DELETE
```

### Database Indexes
```sql
-- Improve query performance
CREATE INDEX idx_projects_category ON projects(category);
CREATE INDEX idx_projects_featured ON projects(is_featured);
CREATE INDEX idx_articles_slug ON articles(slug);
CREATE INDEX idx_articles_category ON articles(category);
CREATE INDEX idx_articles_published ON articles(is_published);
CREATE INDEX idx_articles_publish_date ON articles(publish_date);
```

---

## 📱 Responsive Behavior

### Desktop (1025px+)
- Projects grid: 3 columns
- ProjectsArchive: 3 columns
- ArticlesArchive: 2-column layout
- Featured image: 500px height
- iframe: 600px height

### Tablet (1024px)
- Projects grid: 2 columns
- ProjectsArchive: 2 columns
- ArticlesArchive: 1 column
- Featured image: 400px height
- iframe: 500px height

### Mobile (768px)
- Projects grid: 1 column
- ProjectsArchive: 1 column
- ArticlesArchive: 1 column (stacked)
- Featured image: 300px height
- iframe: 400px height

### Small Mobile (480px)
- All grids: 1 column
- Reduced padding
- Optimized button sizes
- Single column layouts

---

## 🎯 Integration Checklist

### Before Production
- [ ] API integration complete
- [ ] Database migrations ran
- [ ] Sample data loaded
- [ ] Admin users created
- [ ] Environment variables set
- [ ] Redis configured
- [ ] CORS properly configured
- [ ] All routes tested
- [ ] Mobile responsiveness verified
- [ ] Animations working smoothly
- [ ] Error handling tested
- [ ] Security headers configured
- [ ] Database backups setup
- [ ] Monitoring enabled
- [ ] SEO meta tags added

### Deployment
- [ ] Backend deployed
- [ ] Frontend deployed
- [ ] Domain configured
- [ ] SSL certificate installed
- [ ] Cron jobs setup (if needed)
- [ ] Monitoring dashboard configured
- [ ] Error tracking configured
- [ ] Performance monitoring active

---

## 📚 File Reference

### Backend Files
- `app/models/models.py` - Project & Article models
- `app/routers/projects.py` - Projects API routes
- `app/routers/articles.py` - Articles API routes
- `app/schemas/schemas.py` - Pydantic schemas
- `app/cache.py` - Cache configuration
- `main.py` - App initialization

### Frontend Files
- `src/App.vue` - Main app with routing
- `src/components/Projects.vue` - Home page projects
- `src/components/ProjectsArchive.vue` - Projects listing
- `src/components/ProjectDetail.vue` - Project details
- `src/components/ArticlesArchive.vue` - Articles listing
- `src/components/ArticleDetail.vue` - Article details
- `src/components/Header.vue` - Navigation
- `src/components/Footer.vue` - Footer
- `src/styles/animations.css` - Animations

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 on routes | Check hash routing, verify routes in App.vue |
| API errors | Verify backend is running, check API URL |
| No data showing | Ensure sample data is loaded, check console |
| Images not loading | Check image URLs, verify uploads directory |
| Animations not working | Check classes in HTML, verify CSS is imported |
| Mobile layout broken | Check responsive breakpoints, device width |
| Slow loading | Check caching, optimize images, check queries |
| Iframe not displaying | Verify iframe_url is valid, check iframe tag |

---

## 📊 Statistics

### Components Created
- 5 new Vue components
- 2 new API routers
- 2 new database models
- 4 new schema definitions
- Multiple styling improvements

### Lines of Code
- Frontend: ~3000+ lines
- Backend: ~1500+ lines
- Styles: ~1000+ lines
- Total: ~5500+ lines

### Features Implemented
- ✅ Project management system
- ✅ Article publishing system
- ✅ Full-text search
- ✅ Filtering & categorization
- ✅ Pagination
- ✅ Responsive design
- ✅ Animation system
- ✅ iframe support
- ✅ Social sharing
- ✅ Related items suggestion

---

**Last Updated:** 25 دسامبر ۲۰۲۵  
**Version:** 1.0.0  
**Status:** ✅ Ready for Testing & Deployment

