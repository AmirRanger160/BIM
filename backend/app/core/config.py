from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import logging


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "sqlite:///./geobiro.db"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"
    SMTP_FROM_EMAIL: str = "noreply@geobiro.ba"
    ADMIN_EMAIL: str = "info@geobiro.ba"

    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = 'allow'


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    logger.info("Attempting to load settings from environment variables.")
    try:
        settings = Settings()
        logger.info("Settings loaded successfully.")
        logger.debug(f"Settings: {settings.dict()}")
        return settings
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        raise
