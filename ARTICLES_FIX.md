# حل مشکل نمایش مقالات

## مشکل:
مقالات در آرشیو و صفحه جزئیات مقالات نمایش داده نمی‌شوند.

## دلیل:
دیتابیس هیچ مقاله‌ای ندارد. اپلیکیشن فقط مقالات منتشرشده را نمایش می‌دهد (`is_published == True`).

## حل:

### روش 1: استفاده از API (بهترین راه برای توسعه)

```bash
# 1. سرور بکند را شروع کنید
cd backend
python3 main.py

# 2. در ترمینال جدید، مقالات را seed کنید
curl -X POST http://localhost:8000/api/articles/seed-demo
```

**نتیجه:**
```json
{
  "message": "Successfully seeded 5 demo articles",
  "count": 5
}
```

### روش 2: استفاده از Admin Panel
1. وارد Admin Panel شوید
2. به Content Management → Articles بروید
3. مقالات را دستی اضافه کنید

## تغییرات انجام‌شده:

### Backend (`/backend/app/routers/articles.py`):
- ✅ endpoint جدید اضافه شد: `POST /api/articles/seed-demo`
- این endpoint برای توسعه مقالات نمونه را اضافه می‌کند
- به احراز هویت نیاز ندارد (فقط برای توسعه)

### Frontend:
- ✅ Frontend دوباره ساخت شد
- ✅ Assets با backend sync شد

## تست کردن:

پس از seed کردن مقالات:

1. **صفحه اصلی:** مقالات برجسته باید نمایش داده شوند
2. **صفحه آرشیو:** تمام مقالات منتشرشده باید نمایش داده شوند
3. **صفحه جزئیات:** با کلیک بر هر مقاله، جزئیات کامل نمایش داده شود

## نکات مهم:

- endpoint `seed-demo` فقط اگر مقالاتی وجود نداشته باشند کار می‌کند
- مقالات منتشرشده فقط با `is_published = True` نمایش داده می‌شوند
- برای حذف مقالات، از Admin Panel استفاده کنید یا دیتابیس را پاک کنید

## فایل‌های تغییر یافته:
- `backend/app/routers/articles.py` - endpoint seed اضافه شد
- `backend/static/` - frontend sync شد
