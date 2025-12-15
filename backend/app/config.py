import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """تنظیمات برنامه"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'  # نادیده گرفتن فیلدهای اضافی
    )
    
    # App
    APP_NAME: str = "BIM Backend API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./bim.db"
    
    # Security
    SECRET_KEY: str = "bim-secret-key-change-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    FRONTEND_URL: str = "https://probable-doodle-45g6r4grp452qgq-3001.app.github.dev"
    ALLOWED_ORIGINS: list = [
        "https://probable-doodle-45g6r4grp452qgq-3001.app.github.dev",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Admin
    ADMIN_EMAIL: str = "admin@bim.com"
    ADMIN_PASSWORD: str = "admin123"


settings = Settings()
