# راهنمای سریع استقرار در Liara

## ✨ خصوصیات جدید

- ✅ Admin user خودکار
- ✅ Database initialization خودکار
- ✅ Health check بهتر

## مراحل استقرار:

### 1. آماده‌سازی

```bash
# Clone یا sync repository
cd /home/unique/projects/BIM

# متأکد شوید backend/Dockerfile و liara.json موجود است
ls -la backend/Dockerfile
ls -la backend/liara.json
ls -la backend/entrypoint.sh
```

### 2. نصب Liara CLI

```bash
npm install -g @liara/cli
```

### 3. Login به Liara

```bash
liara login
```

### 4. Deploy

```bash
cd backend
liara deploy
```

### 5. تنظیمات بعد از Deploy

در Liara Dashboard:

1. **Environment Variables** (اختیاری - مقادیر پیش‌فرض موجود است):
```
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@geobiro.ba
ADMIN_PASSWORD=Admin@123456
SECRET_KEY=<generate-random-secret-key-min-32-chars>
ALGORITHM=HS256
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<your-email>
SMTP_PASSWORD=<your-app-password>
FRONTEND_URL=<your-frontend-domain>
```

2. **Disks** را تخصیص دهید:
   - `data`: 1GB برای SQLite database
   - `uploads`: 5GB برای فایل‌های آپلود

3. **Health Check** را بررسی کنید:
   - سرویس باید در `Healthy` state باشد

## 🔐 اولین Login

پس از اولین deployment:

```bash
Username: admin
Password: Admin@123456  (یا مقدار ADMIN_PASSWORD)
```

**⚠️ توصیه**: پس از login اول، رمز عبور را تغییر دهید

## بررسی وضعیت

```bash
# لاگ‌ها
liara logs

# معلومات سرویس
liara get-app-info

# بررسی URL
curl https://<app-url>/health
```

## مشکلات و حل‌ها

### مشکل: "ناسالم" (Unhealthy)

```bash
liara logs

# اگر مشکل initialization است:
liara deploy --rebuild
```

### مشکل: Database errors

Disk `data` تخصیص داده شده است؟
- Liara Dashboard → Disks
- `data` disk: 1GB
- Mount path: `/app/data`

### مشکل: Admin user ایجاد نشد

```bash
liara exec backend python init_admin.py
```

## سرویس‌های پشتیبانی شده

- ✅ FastAPI with SQLite
- ✅ Automatic Admin User
- ✅ No Redis required
- ✅ File uploads
- ✅ Email notifications
- ✅ JWT authentication

## فایل‌های مهم

```
backend/
├── Dockerfile              ← Container configuration
├── entrypoint.sh          ← Startup script
├── init_admin.py          ← Admin initialization
├── liara.json            ← Liara config
├── requirements.txt      ← Python dependencies
└── main.py              ← FastAPI entry
```

## نکات مهم

1. ✅ Database پایدار است در `/app/data`
2. ✅ Admin user خودکار ایجاد می‌شود
3. ✅ Environment variables از liara.json
4. ✅ Health check هر 30 ثانیه

## اگر هنوز مشکل است

```bash
# Force rebuild
liara deploy --rebuild

# View detailed logs
liara logs -f

# مزیدمعلومات
cat ADMIN_AUTO_CREATE.md
```

برای سوالات بیشتر:
- [Liara Docs](https://docs.liara.ir)
- [FastAPI Docs](https://fastapi.tiangolo.com)
