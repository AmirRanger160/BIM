import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.database import engine
from app.models.models import Base
from app.cache import init_redis
from app.routers import auth, services, team, certificates, licenses, contact, projects, articles, users, upload

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize settings
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # Startup
    logger.info("🚀 Starting GeoBiro FastAPI Backend")
    init_redis()
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down GeoBiro FastAPI Backend")


# Exception handlers (define before using in app initialization)
def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded."""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests. Please try again later."}
    )


# Create FastAPI app
app = FastAPI(
    title="GeoBiro API",
    description="FastAPI backend for GeoBiro website",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code} for {request.method} {request.url}")
    return response


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:8000",
        "http://127.0.0.1:8000",
        "*"  # Allow all origins for development (restrict in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# General exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


# Mount static files for uploads
import os
uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Mount static files for frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    # Mount assets separately
    assets_dir = os.path.join(static_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(articles.router, prefix="/api")
app.include_router(team.router, prefix="/api")
app.include_router(certificates.router, prefix="/api")
app.include_router(licenses.router, prefix="/api")
app.include_router(contact.router, prefix="/api")
app.include_router(users.router, prefix="/api")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }

# Check video endpoint
@app.get("/check_video")
async def check_video():
    static_file_path = os.path.join(static_dir, "video-1080-2.mp4")
    exists = os.path.exists(static_file_path)
    is_file = os.path.isfile(static_file_path) if exists else False
    size = os.path.getsize(static_file_path) if is_file else 0
    return {
        "exists": exists,
        "path": static_file_path,
        "is_file": is_file,
        "size": size,
        "files_in_static": os.listdir(static_dir) if os.path.exists(static_dir) else []
    }


# SPA fallback: serve index.html for non-API routes
@app.get("/{path:path}")
async def serve_spa(path: str):
    """Serve the Vue.js SPA for client-side routing."""
    logger.info(f"Serving path: {path}")
    if path.startswith(("api/", "uploads/", "assets/")):
        logger.info(f"Path starts with excluded prefix: {path}")
        raise HTTPException(status_code=404, detail="Not found")

    # Check if it's a static file
    static_file_path = os.path.join(static_dir, path)
    logger.info(f"Checking static file: {static_file_path}, exists: {os.path.exists(static_file_path)}, isfile: {os.path.isfile(static_file_path)}")
    if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
        logger.info(f"Serving static file: {static_file_path}")
        return FileResponse(static_file_path)

    # Otherwise, serve SPA
    index_path = os.path.join(static_dir, "index.html")
    logger.info(f"Serving SPA index: {index_path}, exists: {os.path.exists(index_path)}")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Not found")


# Root endpoint
@app.get("/")
async def root():
    """Serve the Vue.js SPA."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "Welcome to GeoBiro API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
