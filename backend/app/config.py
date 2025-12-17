import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List


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
    
    # CORS - Dynamic configuration
    FRONTEND_URL: Optional[str] = None
    ALLOWED_ORIGINS: Optional[List[str]] = None
    
    def get_allowed_origins(self) -> List[str]:
        """Get allowed origins dynamically based on environment"""
        if self.ALLOWED_ORIGINS:
            return self.ALLOWED_ORIGINS
        
        allowed = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8080",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8080",
        ]
        
        # Add GitHub Codespaces URLs if in that environment
        if os.getenv("CODESPACES") == "true":
            allowed.extend([
                "https://*.app.github.dev",
            ])
        
        # Add environment-specific URL
        if self.FRONTEND_URL:
            allowed.append(self.FRONTEND_URL)
        
        return allowed
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Admin
    ADMIN_EMAIL: str = "admin@bim.com"
    ADMIN_PASSWORD: str = "admin123"


settings = Settings()
