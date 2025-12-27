# استقرار Backend در Liara

## پیش‌نیازها
- حساب کاربری Liara
- نصب CLI Liara: `npm install -g @liara/cli`

## تنظیمات

### 1. متغیرهای محیطی (Environment Variables)

پس از نصب برنامه در Liara، متغیرهای محیطی زیر را تنظیم کنید:

```
DATABASE_URL=sqlite:///./geobiro.db
SECRET_KEY=<your-secret-key-min-32-chars>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<your-email@gmail.com>
SMTP_PASSWORD=<your-app-password>
SMTP_FROM_EMAIL=noreply@geobiro.ba
ADMIN_EMAIL=info@geobiro.ba
FRONTEND_URL=<your-frontend-url>
ENVIRONMENT=production
DEBUG=False
```

### 2. دیسک‌ها (Disks)

برنامه نیاز به دو دیسک دارد:
- **data**: برای فایل پایگاه داده SQLite (1GB)
- **uploads**: برای فایل‌های آپلود شده (5GB)

در فایل `liara.json` تعریف شده‌اند.

### 3. استقرار

#### روش 1: استفاده از CLI

```bash
cd backend
liara deploy
```

#### روش 2: اتصال به Git

```bash
git remote add liara https://git.liara.ir/<project-id>/backend.git
git push liara main
```

## ساختار پروژه

```
backend/
├── Dockerfile          # Docker configuration
├── .dockerignore       # Files to ignore in Docker
├── liara.json         # Liara configuration
├── .env.example       # Environment variables template
├── requirements.txt   # Python dependencies
├── main.py           # FastAPI entry point
├── app/
│   ├── core/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── services/
├── uploads/          # Upload directory (persistent disk)
└── data/            # SQLite database (persistent disk)
```

## پایگاه داده

برنامه از **SQLite** استفاده می‌کند. پایگاه داده بر روی دیسک پایدار (`/app/data/geobiro.db`) ذخیره می‌شود.

### مقداردهی اولیه

پس از اولین استقرار، می‌توانید داده‌ها را مقداردهی کنید:

```bash
liara exec backend python backend/seed_articles.py
liara exec backend python backend/seed_services.py
```

## بررسی وضعیت

```bash
# لاگ‌های برنامه
liara logs

# بررسی سلامت
curl https://<app-url>/health
```

## مشکلات رایج

### 1. خطای "Module not found"
- متأکد شوید `requirements.txt` تمام وابستگی‌ها دارد
- دوباره build کنید: `liara deploy --rebuild`

### 2. خطای دسترسی به دیسک
- دیسک‌ها باید در Liara تخصیص داده شوند
- مسیرهای mount باید مطابق `liara.json` باشند

### 3. خطای پایگاه داده
- متأکد شوید مسیر `DATABASE_URL` درست است
- دیسک پایدار باید کافی باشد

## اطلاعات بیشتر

- [مستندات Liara](https://docs.liara.ir)
- [مستندات FastAPI](https://fastapi.tiangolo.com)
- [مستندات SQLite](https://www.sqlite.org)
