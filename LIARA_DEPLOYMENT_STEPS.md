# استقرار Backend BIM در Liara - مرحله به مرحله

## ✨ ویژگی‌های نسخه جدید

1. ✅ **Admin user خودکار** - بدون دستور اضافی
2. ✅ **Database initialization خودکار** - هنگام startup
3. ✅ **Health check بهتر** - استفاده از curl
4. ✅ **Entrypoint script** - کنترل بیشتر بر startup

## 🚀 مراحل سریع

### 1. آماده‌سازی

```bash
cd /home/unique/projects/BIM

# متأکد شوید فایل‌های ضروری موجود هستند
ls -la backend/Dockerfile
ls -la backend/entrypoint.sh
ls -la backend/init_admin.py
ls -la backend/liara.json
```

### 2. نصب Liara CLI

```bash
npm install -g @liara/cli
```

### 3. Deploy

**گزینه 1: استفاده از اسکریپت (توصیه شده)**

```bash
./deploy-to-liara.sh
```

**گزینه 2: دستی**

```bash
cd backend
liara deploy
```

### 4. بررسی وضعیت

```bash
# مشاهده لاگ‌ها
liara logs

# بررسی health check
./backend/check-health.sh

# اگر healthy است:
liara get-app-info
```

### 5. اولین Login

**Credentials**:
```
Username: admin
Password: Admin@123456
```

**⚠️ توصیه**: پس از اولین login، رمز عبور را تغییر دهید

## ⚙️ تنظیمات لازم (اختیاری)

### در Liara Dashboard:

#### Environment Variables (پیش‌فرض موجود است)

اگر می‌خواهید تغییر دهید:

```
ADMIN_USERNAME=your-username
ADMIN_EMAIL=your-email@domain.com
ADMIN_PASSWORD=your-secure-password
SECRET_KEY=<generate-with-openssl-rand-base64-32>
ALGORITHM=HS256
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<your-gmail>
SMTP_PASSWORD=<app-password>
FRONTEND_URL=<your-frontend-domain>
ENVIRONMENT=production
DEBUG=False
```

#### Disks

| Name | Size | Mount Path | Purpose |
|------|------|-----------|---------|
| data | 1GB | /app/data | SQLite database |
| uploads | 5GB | /app/uploads | User uploads |

#### Health Check

- Endpoint: `/health`
- Status: باید `healthy` باشد

## 🔍 تشخیص عیب‌های

### مشکل: "ناسالم" (Unhealthy)

**علائم:**
- سرویس هر 2 دقیقه restart می‌شود
- Health check ناموفق است

**حل:**

1. بررسی لاگ‌ها:
```bash
liara logs --tail 50
```

2. اگر initialization error دیدید:
```bash
cd backend
liara deploy --rebuild
```

3. اگر admin user ایجاد نشد:
```bash
liara exec backend python init_admin.py
```

4. اگر database lock دارید:
```bash
liara exec backend rm /app/data/geobiro.db
liara deploy --rebuild
```

### مشکل: Timeout

```bash
# Rebuild with more time
liara deploy --rebuild
```

### مشکل: Upload files

اطمینان دهید disk `uploads` تخصیص داده شده است

## 📝 دستورات مفید

```bash
# نمایش لاگ‌ها (زنده)
liara logs -f

# اطلاعات سرویس
liara get-app-info

# اجرای دستور در سرویس
liara exec backend python init_admin.py

# SSH به سرویس
liara shell

# حذف و استقرار دوباره
liara destroy
liara deploy

# Rebuild (بدون cache)
liara deploy --rebuild

# بررسی وضعیت
liara status
```

## 🔐 تولید SECRET_KEY

```bash
# Linux/Mac
openssl rand -base64 32

# یا استفاده از Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 📊 Startup Flow

```
1. Docker starts
   ↓
2. entrypoint.sh runs
   ├─ Creates directories
   ├─ Calls init_admin.py
   │  ├─ Creates database tables
   │  └─ Creates admin user
   └─ Starts uvicorn
   ↓
3. Health check starts
   ↓
4. API ready
```

## 🛠️ ساختار فایل‌ها

```
backend/
├── Dockerfile              ✅ ENTRYPOINT
├── entrypoint.sh          ✅ Startup script
├── init_admin.py          ✅ Admin init
├── liara.json            ✅ Config
├── requirements.txt      ✅ Dependencies
├── main.py              ✅ FastAPI
└── .env.example         ✅ Template
```

## 🎯 نکات مهم

| چیز | مقدار | یادداشت |
|-----|-------|--------|
| Python | 3.11 | Slim Bookworm |
| Database | SQLite | File-based |
| Port | 8000 | داخلی |
| Health Check | /health | هر 30s |
| Start Period | 10s | زمان شروع |
| Entrypoint | entrypoint.sh | خودکار |
| Admin Create | auto | خودکار |

## 📋 Checklist

- [ ] Dockerfile موجود است
- [ ] entrypoint.sh موجود است و executable
- [ ] init_admin.py موجود است
- [ ] liara.json تنظیم شده
- [ ] requirements.txt کامل است
- [ ] Health endpoint موجود است
- [ ] Liara CLI نصب شده
- [ ] Login به Liara انجام شده
- [ ] Disks تخصیص داده شده
- [ ] Health check passing است
- [ ] Admin login successful است

## 🚨 اگر هنوز مشکل است

1. **بررسی Dockerfile:**
   ```bash
   docker build -t test-backend ./backend
   docker run -p 8000:8000 test-backend
   ```

2. **بررسی entrypoint:**
   ```bash
   cd backend
   bash entrypoint.sh
   ```

3. **بررسی init_admin:**
   ```bash
   cd backend
   python init_admin.py
   ```

4. **مخاطبات:**
   - [Liara Support](https://liara.ir)
   - [FastAPI Docs](https://fastapi.tiangolo.com)
   - فایل ADMIN_AUTO_CREATE.md

## ✨ بعد از موفقیت

1. سایت بررسی کنید: `https://<app-url>`
2. API documentation بررسی کنید: `https://<app-url>/api/docs`
3. Health status بررسی کنید: `https://<app-url>/health`
4. Admin dashboard بررسی کنید: `https://<app-url>/admin`
5. Logs تحت نظر بگذارید برای 24 ساعت اول

