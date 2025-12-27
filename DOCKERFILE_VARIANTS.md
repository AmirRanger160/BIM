# Dockerfile Variants - اختیارات مختلف

## 📌 Backend Only (توصیه شده)

**فایل**: `backend/Dockerfile`

**استفاده**: برای استقرار فقط backend در Liara

**مزایا**:
- ✅ سبک‌تر (Backend تنها)
- ✅ Deploy سریع‌تر
- ✅ Update سهل‌تر
- ✅ بیشتر flexible برای CI/CD

**استقرار**:
```bash
cd backend
liara deploy
```

---

## 📌 Full Stack (Frontend + Backend)

**فایل**: `Dockerfile.fullstack`

**استفاده**: برای استقرار Frontend و Backend با هم در یک سرویس

**مزایا**:
- ✅ یک سرویس برای هر دو
- ✅ ساده‌تر برای prototyping
- ✅ ارزان‌تر (یک سرویس)

**معایب**:
- ❌ image بزرگ‌تر (Frontend + Backend)
- ❌ Deploy ریز کمی سخت‌تر
- ❌ Update Frontend نیاز به rebuild backend دارد

**استقرار**:
```bash
# از root directory
liara deploy --dockerfile Dockerfile.fullstack
```

---

## 🎯 کدام را بخش؟

### توصیه شده: **Backend Only**

**دلایل**:
1. Frontend می‌تواند بر روی Static Hosting (CDN) deploy شود
2. Backend فقط REST API فراهم می‌کند
3. Update سریع‌تر و مستقل
4. بیشتر scalable

**مثال**:
- Backend: Liara (API)
- Frontend: Vercel/Netlify (Static)

---

### اگر می‌خواهید یک سرویس: **Full Stack**

**مثال**:
```bash
# استقرار به Liara با Full Stack
liara deploy --dockerfile Dockerfile.fullstack
```

---

## 📊 مقایسه

| ویژگی | Backend Only | Full Stack |
|------|------------|-----------|
| Image Size | ~500MB | ~1.5GB |
| Deploy Time | ~2 دقیقه | ~5 دقیقه |
| Update Frontend | ❌ نیاز نیست | ✅ نیاز است rebuild |
| Update Backend | ✅ سریع | ✅ سریع |
| Cost | کم | متوسط |
| Flexibility | بالا | پایین |

---

## 🛠️ استفاده محلی

### Backend Only
```bash
cd backend
docker build -t bim-backend .
docker run -p 8000:8000 bim-backend
```

### Full Stack
```bash
docker build -f Dockerfile.fullstack -t bim-fullstack .
docker run -p 8000:8000 bim-fullstack
```

---

## 📝 نتیجه

**استقرار شما**: 
✅ Backend در Liara (`backend/Dockerfile`)
✅ Frontend می‌تواند جداگانه deploy شود

برای شروع:
```bash
cd backend
liara deploy
```
