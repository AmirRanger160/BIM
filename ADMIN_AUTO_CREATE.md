# تغییرات جدید: ایجاد خودکار Admin User

## ✨ ویژگی‌های جدید

### 1. Entrypoint Script (`entrypoint.sh`)
- ✅ ایجاد دایرکتوری‌های ضروری
- ✅ Initialize database
- ✅ ایجاد admin user خودکار
- ✅ شروع FastAPI

### 2. Admin Initialization (`init_admin.py`)
- ✅ ایجاد جداول database
- ✅ بررسی وجود admin user
- ✅ ایجاد admin user اگر موجود نیست
- ✅ استفاده از environment variables

### 3. Dockerfile بروز شد
- ✅ استفاده از `entrypoint.sh`
- ✅ حذف CMD و استفاده از ENTRYPOINT
- ✅ بهینه‌سازی

### 4. liara.json بروز شد
- ✅ اضافه environment variables
- ✅ مقادیر پیش‌فرض admin

---

## 📋 مقادیر پیش‌فرض Admin

| خصوصیت | مقدار |
|---------|--------|
| Username | `admin` |
| Email | `admin@geobiro.ba` |
| Password | `Admin@123456` |
| Role | Admin (مدیر) |

### تغییر مقادیر پیش‌فرض

در Liara Dashboard → Environment Variables:

```
ADMIN_USERNAME=your-admin-username
ADMIN_EMAIL=your-admin-email@domain.com
ADMIN_PASSWORD=your-secure-password
```

---

## 🚀 مراحل استقرار (تغییر نیافته)

### 1. Deploy

```bash
cd backend
liara deploy
```

### 2. پس از Deploy

- ✅ Database ایجاد می‌شود خودکار
- ✅ Admin user ایجاد می‌شود خودکار
- ✅ API آماده است

### 3. بررسی

```bash
# Health check
curl https://<app-url>/health

# Login با credentials:
curl -X POST https://<app-url>/api/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=Admin@123456"
```

---

## 🔐 امنیت

### ⚠️ توصیات مهم

1. **پس از اولین login**:
   - رمز عبور را تغییر دهید
   - EMAIL را اپدیت کنید

2. **Environment Variables**:
   - در production ADMIN_PASSWORD را عوض کنید
   - از password قوی استفاده کنید

3. **Database**:
   - پایگاه داده روی disk پایدار است
   - Backup منظم بگیرید

---

## 📊 فایل‌های تغییر یافته

```
backend/
├── Dockerfile              ← ✅ ENTRYPOINT
├── entrypoint.sh          ← ✅ NEW
├── init_admin.py          ← ✅ NEW
├── liara.json            ← ✅ Environment vars
├── .dockerignore         ← ✅ بروز شده
└── requirements.txt      ← بدون تغییر
```

---

## 🔄 فلوی Startup

```
1. Docker Container شروع می‌شود
   ↓
2. entrypoint.sh اجرا می‌شود
   ├─ دایرکتوری‌ها ایجاد می‌شوند
   ├─ init_admin.py فراخوانی می‌شود
   │  ├─ جداول ایجاد می‌شوند (اگر موجود نیستند)
   │  └─ admin user ایجاد می‌شود (اگر موجود نیست)
   └─ uvicorn شروع می‌شود
   ↓
3. Health check شروع می‌شود
   ↓
4. API آماده است
```

---

## 🧪 تست محلی

```bash
# ساخت image
cd backend
docker build -t bim-backend .

# اجرا
docker run -p 8000:8000 \
  -e ADMIN_USERNAME=admin \
  -e ADMIN_EMAIL=test@example.com \
  -e ADMIN_PASSWORD=TestPass123 \
  bim-backend

# بررسی
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=TestPass123"
```

---

## 🎯 نتیجه

| مرحله | قبل | بعد |
|------|-----|-----|
| Database | ❌ دستی | ✅ خودکار |
| Admin User | ❌ دستی | ✅ خودکار |
| Deploy | 5+ دقیقه | 2-3 دقیقه |
| First Login | ⏳ منتظر setup | ✅ فوری |

---

## 📞 اگر مشکلی بود

```bash
# لاگ‌ها بررسی کنید
liara logs

# اگر admin user ایجاد نشد:
liara exec backend python init_admin.py

# Reset (اگر لازم است):
liara exec backend rm /app/data/geobiro.db
liara deploy --rebuild
```
