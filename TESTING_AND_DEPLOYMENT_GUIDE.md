# راهنمای تست و استقرار

## ✅ اجزای پیاده‌سازی شده

### Backend Components
- ✅ Project Model (Database)
- ✅ Article Model (Database)
- ✅ Projects API Router (/api/projects)
- ✅ Articles API Router (/api/articles)
- ✅ Schemas for validation
- ✅ Cache keys for performance
- ✅ Router registration in main.py

### Frontend Components
- ✅ Projects.vue (صفحه اصلی - بخش پروژه‌ها)
- ✅ ProjectsArchive.vue (آرشیو پروژه‌ها)
- ✅ ProjectDetail.vue (جزئیات پروژه)
- ✅ ArticlesArchive.vue (آرشیو مقالات)
- ✅ ArticleDetail.vue (جزئیات مقاله)
- ✅ App.vue routing system
- ✅ Header.vue navigation links

---

## 🚀 مراحل تست

### ۱. تست Frontend (بدون API)

```bash
cd /home/unique/projects/BIM
npm run dev
```

سپس در مرورگر:
- `http://localhost:5173/` - صفحه اصلی (بخش پروژه‌ها نمایش داده می‌شود)
- `http://localhost:5173/#projects-archive` - آرشیو پروژه‌ها
- `http://localhost:5173/#project/1` - جزئیات پروژه
- `http://localhost:5173/#articles` - آرشیو مقالات
- `http://localhost:5173/#article/bim-benefits-2024` - جزئیات مقاله

**Expected:** تمام صفحات با نمونه‌ داده‌های sample باید نمایش داده شوند.

### ۲. تست Backend Database

```bash
cd /home/unique/projects/BIM/backend

# ۱. ایجاد database migrations
# (اگر از Alembic استفاده می‌کنید)
alembic revision --autogenerate -m "Add Project and Article models"
alembic upgrade head

# ۲. شروع backend
docker compose up --build
# یا
uvicorn main:app --reload
```

### ۳. تست API Endpoints

```bash
# لیست پروژه‌ها
curl http://localhost:8000/api/projects

# فیلتر پروژه‌ها بر اساس دسته‌بندی
curl http://localhost:8000/api/projects?category=BIM

# جزئیات یک پروژه
curl http://localhost:8000/api/projects/1

# لیست مقالات
curl http://localhost:8000/api/articles?skip=0&limit=10

# جزئیات یک مقاله
curl http://localhost:8000/api/articles/1

# جستجو مقالات بر اساس تگ
curl "http://localhost:8000/api/articles?tag=BIM"

# تمام تگ‌های موجود
curl http://localhost:8000/api/articles/tags/all
```

### ۴. تست Admin Panel (ایجاد/ویرایش/حذف)

```bash
# ابتدا کاربر Admin ایجاد کنید
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@geobiro.com",
    "password": "securepassword123"
  }'

# لاگین
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "securepassword123"
  }' | jq -r '.access_token')

# ایجاد پروژه جدید
curl -X POST http://localhost:8000/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title_en": "New BIM Project",
    "title_fa": "پروژه BIM جدید",
    "description_en": "Description...",
    "description_fa": "توضیحات...",
    "category": "BIM",
    "image_url": "https://example.com/image.jpg"
  }'

# ایجاد مقاله جدید
curl -X POST http://localhost:8000/api/articles \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title_en": "Article Title",
    "title_fa": "عنوان مقاله",
    "slug": "article-slug",
    "summary_en": "Summary...",
    "summary_fa": "خلاصه...",
    "content_en": "<p>Content...</p>",
    "content_fa": "<p>متن...</p>",
    "category": "BIM",
    "tags": "BIM, Technology, News"
  }'
```

---

## 📋 Checklist تست

### Frontend Testing
- [ ] صفحه اصلی بارگذاری می‌شود
- [ ] بخش پروژه‌ها نمایش داده می‌شود (۶ کارت)
- [ ] لینک‌های navigation کار می‌کنند
- [ ] صفحه آرشیو پروژه‌ها بارگذاری می‌شود
- [ ] فیلتر دسته‌بندی کار می‌کند
- [ ] صفحه جزئیات پروژه بارگذاری می‌شود
- [ ] iframe (اگر موجود باشد) نمایش داده می‌شود
- [ ] صفحه آرشیو مقالات بارگذاری می‌شود
- [ ] جستجو در مقالات کار می‌کند
- [ ] Pagination کار می‌کند
- [ ] صفحه جزئیات مقاله بارگذاری می‌شود
- [ ] دکمه‌های اشتراک‌گذاری کار می‌کنند

### Backend Testing
- [ ] Database tables ایجاد می‌شوند
- [ ] API endpoints پاسخ می‌دهند
- [ ] Pagination کار می‌کند
- [ ] Filtering کار می‌کند
- [ ] Caching کار می‌کند (Redis)
- [ ] Admin authentication کار می‌کند
- [ ] CRUD operations موفق هستند

### Design Testing
- [ ] Responsive design (Desktop, Tablet, Mobile)
- [ ] Animations نمایش داده می‌شوند
- [ ] RTL support صحیح است
- [ ] رنگ‌ها سازگار هستند
- [ ] Borders و spacing درست هستند

---

## 🔧 Debugging

### مسائل رایج

**مسئله:** "404 Not Found" برای routes
```
**حل:** مطمئن شوید که hash routing صحیح کار می‌کند
```

**مسئله:** Sample data نمایش داده نمی‌شود
```
**حل:** کنسول مرورگر را بررسی کنید برای خطاهای JavaScript
```

**مسئله:** API connection error
```
**حل:** مطمئن شوید که backend در حال اجرا است
- Backend URL: http://localhost:8000
- Frontend URL: http://localhost:5173
```

**مسئله:** Database tables موجود نیستند
```
**حل:** 
# ایجاد tables با Python directly
python3 -c "
from app.database import engine
from app.models.models import Base
Base.metadata.create_all(bind=engine)
print('Tables created successfully')
"
```

---

## 📊 Sample Data

### پروژه‌های نمونه

| ID | عنوان فارسی | دسته‌بندی | تصویر | iframe |
|----|----------|--------|-----|--------|
| 1 | پروژه مدل‌سازی BIM | BIM | ✓ | ✗ |
| 2 | پردازش ابر نقطه سه‌بعدی | Surveying | ✓ | ✓ |
| 3 | تحلیل نقشه‌برداری شهری | Surveying | ✓ | ✗ |
| 4 | ارزیابی نوسازی | BIM | ✓ | ✗ |
| 5 | نقشه‌برداری زیرساخت | Surveying | ✓ | ✗ |
| 6 | BIM مجتمع صنعتی | BIM | ✓ | ✗ |

### مقالات نمونه

| ID | عنوان فارسی | دسته‌بندی | تاریخ |
|----|----------|--------|------|
| 1 | فوایدی فناوری BIM در ساخت و ساز مدرن | BIM | 1401-10-24 |
| 2 | راهنمای کامل اسکن لیزری و ابر نقاط | Surveying | 1401-10-19 |
| 3 | فناوری دیجیتال دوقلو در املاک | Technology | 1401-10-14 |
| 4 | استانداردهای نقشه‌برداری جدید | News | 1401-10-07 |
| 5 | مقایسه نرم‌افزار BIM: Revit vs ArchiCAD | BIM | 1401-09-29 |
| 6 | پروژه‌های جدید به پورتفولیو | News | 1401-09-24 |

---

## 📱 Responsive Breakpoints

```css
Desktop:    >= 1025px    (3 columns)
Tablet:     1024px       (2 columns)
Mobile:     768px        (1 column)
Small:      <= 480px     (optimized)
```

---

## 🎨 رنگ‌های مستخدم

```
Primary:        #1abc9c  (Teal - دکمه‌ها، لینک‌ها)
Dark:           #1a1a1a  (متن اصلی)
Gray:           #666     (متن ثانوی)
Light Gray:     #f9f9f9  (backgrounds)
Border:         #e8e8e8  (borders)
Error:          #d32f2f  (خطاها)
Success:        #1abc9c  (موفقیت)
```

---

## 🔒 Security Notes

✅ Admin endpoints محافظت‌شده با JWT  
✅ Database models validated with Pydantic  
✅ CORS configured properly  
✅ SQL injection protected (SQLAlchemy ORM)  
✅ XSS protection (Vue escaping)  

---

## 📈 Performance

✅ Redis caching enabled  
✅ Database indexes on key fields  
✅ Lazy loading in images  
✅ GPU-accelerated animations  
✅ Pagination for large datasets  
✅ Efficient database queries  

---

## 📞 Support & Questions

برای سؤالات یا مشکلات:
1. بررسی کنید که تمام فایل‌ها به‌روز شده‌اند
2. Console browser را برای خطاهای JavaScript بررسی کنید
3. Backend logs را برای API errors بررسی کنید
4. Database connection صحیح است؟

