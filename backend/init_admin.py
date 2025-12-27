#!/usr/bin/env python
"""
Initialize database and create default admin user
Runs automatically on startup
"""

import logging
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app.models.models import Base, User
from app.core.config import get_settings
from app.core.security import hash_password

def init_database():
    """Initialize database tables"""
    logger.info("📊 Creating database tables...")
    
    settings = get_settings()
    
    # Create engine
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    )
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created")
    
    return engine

def create_admin_user(engine):
    """Create default admin user if it doesn't exist"""
    logger.info("👤 Checking for admin user...")
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        settings = get_settings()
        
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin").first()
        
        if admin:
            logger.info("✅ Admin user already exists")
            return
        
        # Create admin user with default credentials
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@geobiro.ba")
        admin_password = os.getenv("ADMIN_PASSWORD", "Admin@123")
        
        logger.info(f"🔐 Creating admin user: {admin_username}")
        
        admin_user = User(
            username=admin_username,
            email=admin_email,
            hashed_password=hash_password(admin_password),
            is_admin=True,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        logger.info(f"✅ Admin user created successfully!")
        logger.info(f"   Username: {admin_username}")
        logger.info(f"   Email: {admin_email}")
        logger.info(f"   🔐 Change password immediately after first login!")
        
    except Exception as e:
        logger.error(f"❌ Error creating admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def main():
    """Main initialization function"""
    logger.info("=" * 60)
    logger.info("🚀 Database Initialization")
    logger.info("=" * 60)
    
    try:
        # Create database tables
        engine = init_database()
        
        # Create admin user
        create_admin_user(engine)
        
        logger.info("=" * 60)
        logger.info("✅ Initialization completed successfully!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Initialization failed: {e}")
        logger.error("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
