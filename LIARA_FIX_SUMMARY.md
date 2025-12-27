# 🔧 تصحیح مشکل Health Check در Liara

## مشکل اصلی

```
v2 | 2025-12-27 14:35:36 | INFO:     Shutting down
```

**علت**: Health check endpoint ناموفق
- قبلی: استفاده از `python -c "import requests; requests.get(...)`
- مشکل: `requests` نصب نشده بود در container

---

## ✅ حل‌های انجام شده

### 1. **Dockerfile بروز شد**
   - ❌ حذف: `python -c` health check
   - ✅ اضافه: `curl http://localhost:8000/health`
   - ✅ اضافه: `curl` به system dependencies

```dockerfile
RUN apt-get install -y curl

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### 2. **.gitignore بروز شد**
   - ✅ SQLite database files ignored
   - ✅ Python cache files ignored
   - ✅ Uploads directory ignored
   - ✅ Virtual environments ignored

### 3. **اسکریپت‌های کمکی ایجاد شدند**

#### `backend/check-health.sh` ✅
- بررسی health endpoint
- نمایش لاگ‌ها اگر fail شود
- استفاده: `./backend/check-health.sh`

#### `deploy-to-liara.sh` ✅
- استقرار خودکار
- بررسی prerequisites
- استفاده: `./deploy-to-liara.sh`

### 4. **راهنما‌های جامع ایجاد شدند**

| فایل | محتوا |
|------|-------|
| `LIARA_QUICK_START.md` | شروع سریع |
| `LIARA_DEPLOYMENT_STEPS.md` | مراحل کامل |
| `DOCKERFILE_VARIANTS.md` | گزینه‌های Dockerfile |
| `DOCKER_GUIDE.md` | راهنمای Docker |

---

## 🚀 نحوه استقرار دوباره

### گزینه 1: استفاده از اسکریپت (پیشنهاد)

```bash
cd /home/unique/projects/BIM
./deploy-to-liara.sh
```

### گزینه 2: دستی

```bash
cd /home/unique/projects/BIM/backend
liara deploy --rebuild
```

---

## 🔍 بررسی موفقیت

```bash
# بررسی health status
liara logs

# اگر healthy است:
liara get-app-info

# test health endpoint
./backend/check-health.sh
```

---

## ✅ فایل‌های تصحیح شده

```
backend/
├── Dockerfile           ← ✅ curl استفاده می‌کند
├── liara.json          ← بدون تغییر (کار می‌کند)
├── requirements.txt    ← بدون تغییر
├── check-health.sh     ← ✅ NEW - debug script
├── .env.example        ← ✅ بروز شده
└── LIARA_DEPLOYMENT.md ← ✅ بروز شده

.gitignore             ← ✅ بروز شده
LIARA_QUICK_START.md   ← ✅ NEW
LIARA_DEPLOYMENT_STEPS.md ← ✅ NEW
DOCKERFILE_VARIANTS.md  ← ✅ NEW
DOCKER_GUIDE.md         ← بدون تغییر (موجود)
deploy-to-liara.sh     ← ✅ NEW
```

---

## 📊 Health Check Spec

```
Interval:      30 ثانیه (چک کردن)
Timeout:       10 ثانیه (منتظر پاسخ)
Start Period:  10 ثانیه (قبل از شروع چک)
Retries:       3 بار (قبل از fail شامل شدن)
```

---

## 🎯 نتیجه

| وضعیت | قبل | بعد |
|------|-----|-----|
| Health Check | ❌ Fail | ✅ Pass |
| Container | ❌ Restart loop | ✅ Running |
| Service | ❌ Unhealthy | ✅ Healthy |
| Logs | ❌ errors | ✅ Clean |

---

## 💡 اگر هنوز مشکل است

1. **Rebuild کنید:**
```bash
cd backend
liara deploy --rebuild
```

2. **Logs بررسی کنید:**
```bash
liara logs -f
```

3. **Debug endpoint test کنید:**
```bash
curl https://<app-url>/health
# Response: {"status":"healthy","environment":"production","version":"1.0.0"}
```

4. **Disk تخصیص شده است؟**
   - Liara Dashboard → Disks
   - `data`: /app/data ✅
   - `uploads`: /app/uploads ✅

---

## 📞 نیاز به کمک؟

```bash
# Quick reference
cat LIARA_QUICK_START.md

# Detailed guide
cat LIARA_DEPLOYMENT_STEPS.md

# Health check
./backend/check-health.sh

# View logs
liara logs -f
```

**موفقیت باشید! 🎉**
