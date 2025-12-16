from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import settings
from app.database import init_db, get_db
from app.routes import articles, gallery, other, auth_routes, upload, admin, comments, videos
from app import models, auth, schemas
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """مدیریت lifecycle برنامه"""
    # Startup
    print("🚀 Starting BIM Backend API...")
    
    # ایجاد جداول دیتابیس
    init_db()
    print("✅ Database initialized")
    
    # ایجاد کاربر ادمین اولیه
    db = next(get_db())
    try:
        admin_user = auth.get_user_by_email(db, settings.ADMIN_EMAIL)
        if not admin_user:
            admin_data = schemas.UserCreate(
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD,
                full_name="Admin"
            )
            auth.create_user(db, admin_data, is_admin=True)
            print(f"✅ Admin user created: {settings.ADMIN_EMAIL}")
        else:
            print(f"✅ Admin user exists: {settings.ADMIN_EMAIL}")
        
        # ایجاد داده‌های نمونه اگر دیتابیس خالی است
        create_sample_data(db)
        
    finally:
        db.close()
    
    print(f"✅ Server running on {settings.HOST}:{settings.PORT}")
    
    # Log BACKEND_URL for debugging
    import os
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    print(f"🌐 BACKEND_URL: {backend_url}")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration - Allow all origins in development, restrict in production
allowed_origins = settings.get_allowed_origins()

# Allow wildcard for GitHub Codespaces during development
if os.getenv("CODESPACES") == "true":
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https://.*\.app\.github\.dev",
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        max_age=600,
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        max_age=600,
    )

# Mount static files directory
uploads_dir = Path(__file__).parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

# Mount Vue.js built frontend
# Try two locations: /app/dist (Docker) and ../dist (local development)
frontend_dist = None
possible_paths = [
    Path(__file__).parent / "dist",  # In Docker: /app/dist
    Path(__file__).parent.parent / "dist"  # Local dev: /workspaces/BIM/dist
]

for path in possible_paths:
    if path.exists():
        frontend_dist = path
        print(f"✅ Frontend dist found at: {path}")
        break

if frontend_dist:
    # Mount assets (JS, CSS, etc.)
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    print(f"✅ Frontend assets mounted from {frontend_dist / 'assets'}")
else:
    print(f"⚠️  Frontend dist folder not found")
    print("Run 'npm run build' in the project root to build the frontend")

# Include Routers
app.include_router(auth_routes.router)
app.include_router(articles.router)
app.include_router(gallery.router)
app.include_router(other.router)
app.include_router(upload.router)
app.include_router(admin.router)
app.include_router(comments.router)
app.include_router(videos.router)

@app.get("/")
def root():
    """Root endpoint - serve frontend or API info"""
    # Try two locations: /app/dist (Docker) and ../dist (local development)
    possible_paths = [
        Path(__file__).parent / "dist",  # In Docker: /app/dist
        Path(__file__).parent.parent / "dist"  # Local dev: /workspaces/BIM/dist
    ]
    
    for path in possible_paths:
        index_file = path / "index.html"
        if index_file.exists():
            from fastapi.responses import FileResponse
            return FileResponse(str(index_file), media_type="text/html")
    
    # Fallback to API info
    return {
        "message": "Welcome to BIM Backend API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "frontend": "Not built - run 'npm run build'"
    }


@app.get("/favicon.ico")
def favicon():
    """Serve favicon"""
    from fastapi.responses import FileResponse
    possible_paths = [
        Path(__file__).parent / "dist",  # In Docker: /app/dist
        Path(__file__).parent.parent / "dist"  # Local dev: /workspaces/BIM/dist
    ]
    
    for path in possible_paths:
        favicon_file = path / "favicon.ico"
        if favicon_file.exists():
            return FileResponse(str(favicon_file))
    
    # Return a 404 for favicon if not found
    from fastapi import HTTPException
    raise HTTPException(status_code=404)


@app.get("/robots.txt")
def robots():
    """Serve robots.txt for SEO"""
    from fastapi.responses import FileResponse
    possible_paths = [
        Path(__file__).parent / "dist",  # In Docker: /app/dist
        Path(__file__).parent.parent / "dist"  # Local dev: /workspaces/BIM/dist
    ]
    
    for path in possible_paths:
        robots_file = path / "robots.txt"
        if robots_file.exists():
            return FileResponse(str(robots_file), media_type="text/plain")
    
    # Return a 404 if robots.txt not found
    from fastapi import HTTPException
    raise HTTPException(status_code=404)
    
    # Return a simple robots.txt if file not found
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse("User-agent: *\nDisallow: /api/\nDisallow: /admin/")


@app.get("/sitemap.xml")
def sitemap():
    """Serve sitemap.xml for SEO"""
    from fastapi.responses import FileResponse
    frontend_dist = Path(__file__).parent.parent / "dist"
    sitemap_file = frontend_dist / "sitemap.xml"
    
    if sitemap_file.exists():
        return FileResponse(str(sitemap_file), media_type="application/xml")
    
    from fastapi import HTTPException
    raise HTTPException(status_code=404)


@app.get("/api/config")
def get_config():
    """Get backend configuration"""
    import os
    return {
        "backend_url": os.getenv("BACKEND_URL", "http://localhost:8000"),
        "uploads_enabled": True,
        "max_file_size": 5 * 1024 * 1024
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION
    }


def create_sample_data(db: Session):
    """ایجاد داده‌های نمونه برای تست"""
    
    # بررسی اگر داده وجود دارد
    article_count = db.query(models.Article).count()
    if article_count > 0:
        print("✅ Sample data already exists")
        return
    
    print("📦 Creating sample data...")
    
    # مقالات نمونه
    sample_articles = [
        {
            "title": "آموزش جامع Vue.js 3 از صفر تا صد",
            "excerpt": "یادگیری کامل Vue.js نسخه 3 با Composition API، راوتر و مدیریت state.",
            "full_content": "<h2>مقدمه‌ای بر Vue.js 3</h2><p>Vue.js یکی از محبوب‌ترین فریمورک‌های جاوااسکریپت است...</p>",
            "category": "برنامه‌نویسی",
            "icon": "⚡",
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "author": "محمد رضایی",
            "author_avatar": "م",
            "author_role": "توسعه‌دهنده فرانت‌اند",
            "read_time": "۱۲ دقیقه",
            "featured": True,
            "tags": ["Vue.js", "JavaScript", "Frontend", "Tutorial"],
            "views": 3500
        },
        {
            "title": "اصول طراحی UI/UX برای موبایل",
            "excerpt": "نکات کلیدی در طراحی رابط کاربری موبایل برای بهبود تجربه کاربری.",
            "full_content": "<h2>اهمیت طراحی موبایل</h2><p>امروزه بیش از 70٪ از کاربران از طریق موبایل به وب دسترسی دارند...</p>",
            "category": "طراحی",
            "icon": "🎨",
            "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "author": "سارا احمدی",
            "author_avatar": "س",
            "author_role": "طراح UI/UX",
            "read_time": "۹ دقیقه",
            "featured": True,
            "tags": ["UI/UX", "Design", "Mobile"],
            "views": 4200
        },
        {
            "title": "معرفی هوش مصنوعی ChatGPT و کاربردها",
            "excerpt": "آشنایی با قابلیت‌های ChatGPT و نحوه استفاده از آن در پروژه‌های واقعی.",
            "full_content": "<h2>ChatGPT چیست؟</h2><p>ChatGPT یک مدل زبانی قدرتمند است...</p>",
            "category": "هوش مصنوعی",
            "icon": "🤖",
            "gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
            "author": "فاطمه کریمی",
            "author_avatar": "ف",
            "author_role": "پژوهشگر AI",
            "read_time": "۱۰ دقیقه",
            "featured": False,
            "tags": ["AI", "ChatGPT", "Machine Learning"],
            "views": 5200
        }
    ]
    
    for article_data in sample_articles:
        article = models.Article(**article_data)
        db.add(article)
    
    # گالری نمونه
    sample_gallery = [
        {
            "title": "داشبورد مدیریتی پیشرفته",
            "description": "سیستم جامع مدیریت با امکانات گسترده برای کنترل کامل کسب و کار",
            "icon": "📊",
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "category": "داشبورد",
            "category_color": "#667eea",
            "date": "دی ۱۴۰۳",
            "duration": "۳ ماه",
            "views": 5200,
            "comments": 123,
            "technologies": ["Vue.js", "Node.js", "MongoDB", "Chart.js"]
        },
        {
            "title": "اپلیکیشن موبایل فروشگاهی",
            "description": "اپلیکیشن فروشگاه آنلاین با تجربه کاربری عالی",
            "icon": "📱",
            "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "category": "موبایل اپ",
            "category_color": "#f093fb",
            "date": "آذر ۱۴۰۳",
            "duration": "۴ ماه",
            "views": 7800,
            "comments": 245,
            "technologies": ["React Native", "Redux", "Firebase"]
        }
    ]
    
    for item_data in sample_gallery:
        item = models.GalleryItem(**item_data)
        db.add(item)
    
    # نظرات نمونه
    sample_testimonials = [
        {
            "name": "علی محمدی",
            "role": "مدیرعامل شرکت تکنولوژی پارس",
            "avatar": "ع",
            "text": "کار بسیار حرفه‌ای و تیمی فوق‌العاده. پروژه ما در زمان مقرر تحویل شد.",
            "rating": 5,
            "date": "دی ۱۴۰۴",
            "project": "سیستم مدیریت محتوا",
            "approved": True
        }
    ]
    
    for test_data in sample_testimonials:
        testimonial = models.Testimonial(**test_data)
        db.add(testimonial)
    
    # آمار نمونه
    sample_statistics = [
        {"number": "۱۵۰+", "label": "پروژه موفق", "icon": "🎯", "order": 1},
        {"number": "۹۵%", "label": "رضایت مشتریان", "icon": "⭐", "order": 2},
        {"number": "۵۰+", "label": "مشتری فعال", "icon": "👥", "order": 3},
        {"number": "۸+", "label": "سال تجربه", "icon": "💼", "order": 4}
    ]
    
    for stat_data in sample_statistics:
        stat = models.Statistic(**stat_data)
        db.add(stat)
    
    # گواهینامه‌های نمونه
    sample_certificates = [
        {
            "title": "گواهینامه تخصصی Vue.js",
            "issuer": "Vue School",
            "date": "۲۰۲۳",
            "icon": "⚡",
            "color": "#42b883"
        },
        {
            "title": "گواهینامه AWS Solutions Architect",
            "issuer": "Amazon Web Services",
            "date": "۲۰۲۳",
            "icon": "☁️",
            "color": "#ff9900"
        }
    ]
    
    for cert_data in sample_certificates:
        cert = models.Certificate(**cert_data)
        db.add(cert)
    
    db.commit()
    print("✅ Sample data created successfully")


# Catch-all route for SPA - serve index.html for any unmatched routes
# This must be the LAST route to avoid interfering with API routes
@app.get("/{full_path:path}")
def serve_spa(full_path: str):
    """
    Catch-all route for Vue.js SPA routing
    Serves index.html for client-side routing
    Only called if no other route matches (API routes are matched first)
    """
    # Safeguard: Ensure we're not accidentally serving SPA for reserved paths
    reserved_prefixes = ("api/", "docs", "redoc", "openapi", "uploads/", ".well-known/", "static/")
    if any(full_path.startswith(prefix) for prefix in reserved_prefixes):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not Found")
    
    # Serve index.html for SPA routing (client-side routing)
    possible_paths = [
        Path(__file__).parent / "dist",  # In Docker: /app/dist
        Path(__file__).parent.parent / "dist"  # Local dev: /workspaces/BIM/dist
    ]
    
    for path in possible_paths:
        index_file = path / "index.html"
        if index_file.exists():
            from fastapi.responses import FileResponse
            return FileResponse(str(index_file), media_type="text/html")
    
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Frontend not built - run 'npm run build'")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
