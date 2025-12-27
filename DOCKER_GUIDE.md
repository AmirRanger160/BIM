# راهنمای Docker

## تست محلی با Docker Compose

### 1. نصب Docker
- [Windows & Mac](https://www.docker.com/products/docker-desktop)
- [Linux](https://docs.docker.com/install/)

### 2. ساخت و اجرا

```bash
# ساخت image‌ها
docker-compose -f docker-compose.dev.yml build

# اجرای سرویس‌ها
docker-compose -f docker-compose.dev.yml up

# اجرا در پس‌زمینه
docker-compose -f docker-compose.dev.yml up -d
```

### 3. دسترسی به برنامه

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

### 4. دستورات مفید

```bash
# مشاهده لاگ‌ها
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.dev.yml logs -f frontend

# اجرای دستور در کانتینر
docker-compose -f docker-compose.dev.yml exec backend python seed_articles.py

# توقف سرویس‌ها
docker-compose -f docker-compose.dev.yml down

# حذف volume‌ها
docker-compose -f docker-compose.dev.yml down -v
```

## ساخت و push کردن به Registry

### 1. ساخت image برای production

```bash
cd backend
docker build -t your-registry/bim-backend:latest .
```

### 2. Push به Docker Hub یا Registry شخصی

```bash
docker push your-registry/bim-backend:latest
```

### 3. آزمایش image محلی

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./geobiro.db \
  -e SECRET_KEY=your-secret-key \
  -v bim-data:/app/data \
  -v bim-uploads:/app/uploads \
  your-registry/bim-backend:latest
```

## Dockerfile برای Backend

موقعیت: `backend/Dockerfile`

ویژگی‌ها:
- ✅ Python 3.11 slim
- ✅ SQLite database support
- ✅ Volume support برای data و uploads
- ✅ Health check فعال
- ✅ Environment variables
- ✅ .dockerignore برای بهینه‌سازی

## Volumes

### در docker-compose.dev.yml:

```yaml
volumes:
  ./backend/data:/app/data       # SQLite database
  ./backend/uploads:/app/uploads # Uploaded files
```

### در Liara:

دیسک‌ها در `liara.json` تعریف شده‌اند:
- `data` (1GB): `/app/data`
- `uploads` (5GB): `/app/uploads`

## استقرار در Liara

برای استقرار در Liara:

1. نصب CLI:
```bash
npm install -g @liara/cli
```

2. Login:
```bash
liara login
```

3. Deploy:
```bash
cd backend
liara deploy
```

نکات:
- `Dockerfile` باید در مسیر `backend/` قرار داشته باشد ✓
- `liara.json` باید تنظیم شود ✓
- Disks باید تخصیص داده شوند در Liara control panel

## Troubleshooting

### Build log مشاهده کنید:
```bash
docker-compose -f docker-compose.dev.yml build --no-cache
```

### Container وارد شوید:
```bash
docker-compose -f docker-compose.dev.yml exec backend bash
```

### Database reset کنید:
```bash
docker-compose -f docker-compose.dev.yml exec backend rm /app/data/geobiro.db
```

### Size بررسی کنید:
```bash
docker images
docker system df
```
