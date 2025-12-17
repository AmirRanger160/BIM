# 🚀 راه‌اندازی BIM Application

## مزایا

✅ **یک دستور برای شروع** - فقط یک خط کد  
✅ **بدون نیاز به npm** - در Production فقط Python  
✅ **Frontend + Backend یکجا** - پورت 8000 برای همه  
✅ **Docker Ready** - فقط یک container  

---

## روش اول: Python (توصیه شده)

### نصب Dependencies (یک بار)
```bash
pip install -r backend/requirements.txt
```

### اجرای برنامه
```bash
python3 run.py
```

**و تمام!** برنامه به آدرس `http://localhost:8000` اجرا می‌شود

---

## روش دوم: Shell Script

```bash
cd backend
bash run.sh
```

---

## روش سوم: Docker

### ایجاد و اجرای Container

```bash
docker-compose up --build
```

یا بدون rebuild:
```bash
docker-compose up
```

---

## دسترسی‌ها

| منبع | آدرس |
|------|------|
| **وب‌سایت** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Admin Panel** | http://localhost:8000/admin |
| **Database** | `backend/bim.db` |

---

## مستندات

### پوشه‌های مهم

```
BIM/
├── src/                    # Vue.js Source Files
├── dist/                   # Built Frontend (auto-generated)
├── backend/
│   ├── main.py           # برنامه اصلی
│   ├── app/              # کد اپلیکیشن
│   ├── uploads/          # فایل‌های آپلود شده
│   └── bim.db            # SQLite Database
├── docker-compose.yml    # Docker Configuration
├── run.py               # Python Launcher
└── package.json         # npm Dependencies
```

---

## Environment Variables

```env
DATABASE_URL=sqlite:///./bim.db
BACKEND_URL=http://localhost:8000
PORT=8000
DEBUG=True
```

---

## Troubleshooting

### خطا: "Port 8000 already in use"
```bash
# پیدا کردن process استفاده کننده از پورت 8000
lsof -i :8000

# یا صرفاً
pkill -f uvicorn
```

### Frontend نمایش داده نمی‌شود
```bash
# Frontend را دوباره build کنید
npm run build
```

### Database مشکل دارد
```bash
# Database را پاک کنید (داده‌های جدید ایجاد می‌شود)
rm backend/bim.db
python3 run.py  # دوباره اجرا کنید
```

---

## توسعه (Development)

اگر می‌خواهید Frontend را جداگانه توسعه دهید:

```bash
# Terminal 1: Backend
cd backend
python3 -m uvicorn main:app --reload

# Terminal 2: Frontend
npm run dev
```

---

## تولید (Production)

### Docker (توصیه شده)
```bash
docker-compose up -d
```

### یا Python
```bash
python3 run.py
```

هر دوی این روش‌ها Frontend و Backend را یکجا اجرا می‌کنند.

---

## نکات مهم

1. **Frontend باید build شود**: Frontend اتوماتیکاً build می‌شود اگر `dist/` پوشه موجود نباشد
2. **SQLite Database**: خودکار ایجاد می‌شود
3. **Admin User**: پیش‌فرض است (`admin@bim.com` / `admin`)
4. **Port 8000**: هم Frontend هم Backend از این پورت استفاده می‌کنند

---

## سوالات رایج

**Q: آیا باید npm install کنم؟**  
A: نیست! در Production فقط Python لازم است. `npm run build` اتوماتیکاً هنگام اولین اجرا اجرا می‌شود.

**Q: چطور Database را بکاپ کنم؟**  
A: فایل `backend/bim.db` را کپی کنید.

**Q: آیا می‌تواند درون Docker اجرا شود؟**  
A: بله! فقط `docker-compose up` را اجرا کنید.

---

برای سوالات بیشتر، [مستندات کامل](./README.md) را ببینید.
