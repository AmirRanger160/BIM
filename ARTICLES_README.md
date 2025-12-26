# 📰 راهنمای حل مشکل نمایش مقالات

## خلاصه مشکل
مقالات در آرشیو و صفحات جزئیات نمایش داده نمی‌شدند.

## ریشه‌های مشکل
1. ❌ دیتابیس خالی بود (هیچ مقاله‌ای موجود نبود)
2. ❌ `ArticleDetail.vue` از مقالات سخت‌کدشده استفاده می‌کرد
3. ❌ هیچ راهی برای ایجاد مقالات پایه‌ای وجود نداشت

## ✅ حل‌های اعمال‌شده

### 1. Seed Endpoint برای مقالات
**فایل:** `backend/app/routers/articles.py`

```python
@router.post("/seed-demo")
async def seed_demo_articles(db: Session = Depends(get_db)):
    """5 مقاله نمونه را ایجاد می‌کند"""
```

### 2. ArticleDetail.vue - API Integration
**فایل:** `src/components/ArticleDetail.vue`

- ✅ Import `articleService`
- ✅ حذف مقالات hardcoded
- ✅ استفاده از API برای بارگذاری مقالات
- ✅ محاسبه دینامیکی مقالات مرتبط

### 3. Frontend Rebuilt
```bash
npm run build
✓ dist/assets/index-Bx51-6lN.css
✓ dist/assets/index-aJmPwnwU.js
```

### 4. Assets Synced
```bash
cp -r dist/* backend/static/
```

## 🚀 نحوه استفاده

### مرحله 1: سرور را شروع کنید
```bash
cd backend
python3 main.py
```

### مرحله 2: مقالات را Seed کنید
```bash
# گزینه 1: اسکریپت
./seed-articles.sh

# گزینه 2: curl
curl -X POST http://localhost:8000/api/articles/seed-demo

# گزینه 3: تست خودکار
./test-articles.sh
```

### مرحله 3: فرانتند را شروع کنید
```bash
npm run dev
```

## ✨ نتیجه

بعد از اجرای مراحل بالا:

| صفحه | وضعیت |
|------|--------|
| صفحه اصلی - مقالات برجسته | ✅ کار می‌کند |
| آرشیو مقالات | ✅ تمام مقالات را نمایش می‌دهد |
| صفحه جزئیات مقاله | ✅ محتوای کامل نمایش می‌دهد |
| مقالات مرتبط | ✅ بر اساس دسته‌بندی نمایش داده می‌شود |
| فیلتر و جستجو | ✅ کار می‌کند |

## 📋 API Endpoints

### عمومی
```
GET  /api/articles                    # لیست مقالات
GET  /api/articles/{id_or_slug}       # جزئیات مقاله
GET  /api/articles/tags/all           # تمام برچسب‌ها
POST /api/articles/seed-demo          # Seed مقالات (توسعه)
```

### مدیریت (احراز هویت مورد نیاز)
```
POST   /api/articles                   # ایجاد مقاله
PUT    /api/articles/{id}              # ویرایش مقاله
DELETE /api/articles/{id}              # حذف مقاله
```

## 📝 ساختار مقاله

```json
{
  "id": 1,
  "title_en": "...",
  "title_fa": "...",
  "slug": "article-slug",
  "summary_en": "...",
  "summary_fa": "...",
  "content_en": "<html>...",
  "content_fa": "<html>...",
  "category": "BIM|Surveying|Technology",
  "tags": "tag1, tag2, tag3",
  "author": "نویسنده",
  "image_url": "https://...",
  "is_published": true,
  "publish_date": "2025-01-15T10:00:00",
  "created_at": "...",
  "updated_at": "..."
}
```

## 🛠️ حل مسائل عام

### مقالات نمایش داده نمی‌شوند؟
```bash
# 1. بررسی سرور
curl http://localhost:8000/api/articles

# 2. Seed کردن مقالات
curl -X POST http://localhost:8000/api/articles/seed-demo

# 3. بررسی کنسول مرورگر (F12)
```

### خطای 404 برای مقالات؟
- بررسی کنید سرور بکند اجرا شود
- بررسی کنید پورت 8000 درست باشد

### صفحه جزئیات کار نمی‌کند؟
- اطمینان دهید کہ `articleService` import شده
- بررسی نیم‌خانوادگی مقاله در URL

## 📂 فایل‌های مهم

| فایل | توضیح |
|------|--------|
| `backend/app/routers/articles.py` | Endpoints و seed logic |
| `src/components/ArticleDetail.vue` | صفحه جزئیات مقاله |
| `src/components/ArticlesArchive.vue` | صفحه آرشیو |
| `src/components/FeaturedArticles.vue` | مقالات برجسته |
| `src/services/api.js` | API client |

## 📚 منابع اضافی

- [SOLUTION_ARTICLES_DISPLAY.md](./SOLUTION_ARTICLES_DISPLAY.md) - توضیح فنی کامل
- [ARTICLES_GUIDE.md](./ARTICLES_GUIDE.md) - راهنمای جزئی API
- [backend/QUICK_REFERENCE.md](./backend/QUICK_REFERENCE.md) - مرجع سریع
