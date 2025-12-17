# BIM Application - سیستم مدیریت محتوای BIM

## روش اجرا

### روش 1: با Python (تک فایل)
```bash
# نصب dependencies (یک بار)
pip install -r backend/requirements.txt

# اجرای برنامه
python3 run.py
```

### روش 2: با Bash Script
```bash
# ابتدا npm packages را نصب کنید
npm install

# سپس backend را اجرا کنید
cd backend
bash run.sh
```

### روش 3: با Docker
```bash
# ایجاد و اجرای Docker container
docker-compose up --build

# یا بدون build
docker-compose up
```

## نحوه کار

### Development
1. Frontend و Backend را جداگانه اجرا کنید:
```bash
# Terminal 1: Backend
cd backend
python3 -m uvicorn main:app --reload

# Terminal 2: Frontend
npm run dev
```

### Production (Docker)
```bash
docker-compose up
```

## پیش‌نیازها

- Python 3.11+
- Node.js 18+ (فقط برای development)
- Docker & Docker Compose (برای استفاده از Docker)

## Database

- SQLite (پیش‌فرض): `backend/bim.db`
- خودکار ایجاد می‌شود هنگام اولین اجرا

## نکات مهم

- Frontend اتوماتیکاً در production توسط Backend serve می‌شود
- Frontend و Backend یک عدد port (8000) استفاده می‌کنند
- تمام فایل‌های آپلود شده در `backend/uploads/` ذخیره می‌شوند

## دسترسی‌ها

- **اپلیکیشن**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Admin Panel**: http://localhost:8000/admin

## درباره ساختار

```
BIM/
├── src/                    # Vue.js Frontend
├── dist/                   # Frontend Built Files (auto-generated)
├── backend/               # Python Backend
│   ├── main.py           # Entry point
│   ├── app/              # Application code
│   ├── uploads/          # User uploaded files
│   └── bim.db            # SQLite Database
├── docker-compose.yml    # Docker configuration
├── run.py               # Python startup script
└── package.json         # Frontend dependencies
```
