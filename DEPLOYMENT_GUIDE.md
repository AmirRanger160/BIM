# Deployment Guide - Using Built Vue.js Project

This guide explains how to deploy the BIM project using the built Vue.js frontend served by the FastAPI backend.

## Architecture

```
┌─────────────────────────────────┐
│      Single Server (Port 8000)  │
├─────────────────────────────────┤
│   FastAPI Backend (Python)      │
│   ├── API Routes (/api/*)       │
│   ├── Admin Routes (/admin/*)   │
│   ├── Auth Routes (/auth/*)     │
│   └── Static Frontend (/)       │
│       ├── HTML (index.html)     │
│       ├── JS (assets/*.js)      │
│       ├── CSS (assets/*.css)    │
│       └── Media (robots.txt)    │
└─────────────────────────────────┘
```

## Setup Instructions

### 1. Build the Vue.js Frontend

```bash
# Install dependencies (if not already done)
npm install

# Build the production-ready frontend
npm run build

# This generates the 'dist' folder with:
# - dist/index.html (main entry point)
# - dist/assets/ (bundled JS/CSS)
# - dist/robots.txt (SEO)
# - dist/sitemap.xml (SEO)
```

### 2. Backend Configuration

The backend is already configured to:
- Mount frontend assets at `/assets/`
- Serve `index.html` at `/`
- Handle SPA routing (catch-all for unmatched routes)
- Serve API routes at `/api/`

**Key routes added:**
```python
GET  /              → Serve index.html (frontend)
GET  /favicon.ico   → Serve favicon
GET  /robots.txt    → Serve SEO robots file
GET  /sitemap.xml   → Serve SEO sitemap
GET  /assets/*      → Static JS/CSS/Images
GET  /api/*         → API endpoints
GET  /{full_path}   → SPA catch-all (fallback to index.html)
```

### 3. Start the Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the backend (will serve both API and frontend)
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Visit: `http://localhost:8000`

## Features

### ✅ Frontend Served from Backend
- No separate frontend server needed
- Single origin (no CORS issues)
- Simplified deployment
- Better security

### ✅ API Communication
- Frontend API calls go to `/api/*`
- Axios client automatically detects the correct backend URL
- Works with GitHub Codespaces
- Works with environment variables

### ✅ SPA Routing
- Vue Router works correctly
- All routes fallback to `index.html`
- Browser back/forward buttons work
- Direct URL access works

### ✅ SEO Optimization
- `/robots.txt` for search engines
- `/sitemap.xml` for site indexing
- Proper HTML meta tags in `index.html`

## Development vs Production

### Development
```bash
# Terminal 1: Start backend (serves API)
cd backend && python main.py

# Terminal 2: Start frontend dev server (hot reload)
npm run dev

# Frontend on port 3000 makes API calls to port 8000
```

### Production
```bash
# Build frontend once
npm run build

# Start backend (serves both)
cd backend && python main.py

# Access everything on port 8000
# Frontend: http://localhost:8000
# API: http://localhost:8000/api/*
# Admin Docs: http://localhost:8000/docs
```

## Docker Deployment

### Build Docker Image

```bash
# From project root
docker build -f backend/Dockerfile -t bim-api:latest .
```

The Dockerfile should:
1. Copy the built `dist/` folder
2. Include the built frontend in the Python image
3. Start the FastAPI server

### Run Container

```bash
docker run -p 8000:8000 bim-api:latest
```

## Environment Variables

```bash
# .env or set in system
VITE_API_BASE_URL=http://localhost:8000    # Optional - auto-detected
DATABASE_URL=sqlite:///./bim.db             # Database
ADMIN_EMAIL=admin@bim.com                   # Admin email
ADMIN_PASSWORD=admin123                     # Admin password
DEBUG=true                                  # Debug mode
```

## Troubleshooting

### Build Issues
```bash
# Clear cache and rebuild
rm -rf dist node_modules
npm install
npm run build
```

### API Not Working
- Check that backend is running on port 8000
- Check browser console for CORS errors
- Verify admin token is stored in localStorage

### Routes Not Found
- Make sure `dist/` folder exists
- Rebuild frontend: `npm run build`
- Check server logs for "Frontend dist folder"

### Static Files Not Loading
- Verify `/assets/` mount in backend logs
- Check browser DevTools Network tab for 404s
- Ensure paths in index.html match asset names

## Project Structure

```
BIM/
├── src/                    # Vue.js source
│   ├── App.vue
│   ├── components/
│   ├── views/
│   ├── router/
│   ├── api/
│   └── main.js
├── dist/                   # Built frontend (generated)
│   ├── index.html
│   ├── assets/
│   ├── robots.txt
│   └── sitemap.xml
├── backend/                # FastAPI backend
│   ├── main.py
│   ├── app/
│   └── requirements.txt
├── public/                 # Public assets
├── vite.config.js          # Vite build config
├── package.json            # Frontend dependencies
└── docker-compose.yml      # Docker setup
```

## Performance Optimization

### Frontend
- Vue.js production build: ~320KB (minified)
- CSS optimized: ~26KB gzipped
- No separate HTTP requests for frontend
- Cached assets with hash-based filenames

### Backend
- Static file serving optimized
- API response caching configured
- CORS pre-flight requests minimized
- Assets mounted as static files (fast)

## Next Steps

1. **Build the frontend**: `npm run build`
2. **Start the backend**: `cd backend && python main.py`
3. **Access the app**: http://localhost:8000
4. **Deploy**: Use Docker or deploy to your server

## Support

For issues or questions:
1. Check browser console for errors
2. Check server logs
3. Verify build completed: `ls -la dist/`
4. Check port availability: `lsof -i :8000`
