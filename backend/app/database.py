from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import time
import sys


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


def get_db():
    """Dependency برای دریافت database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(retries: int = 5, delay: int = 3):
    """ایجاد جداول در دیتابیس

    For networked databases (e.g. PostgreSQL) this will retry a few times
    to allow the DB container to become ready when using Docker Compose.
    """
    # If using SQLite just create tables immediately
    if "sqlite" in settings.DATABASE_URL:
        Base.metadata.create_all(bind=engine)
        return

    # For other DBs (Postgres) attempt to connect before creating tables
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            break
        except Exception as exc:
            print(f"⚠️  Database not ready (attempt {attempt}/{retries}): {exc}")
            if attempt == retries:
                print("❌ Could not connect to the database after retries. Exiting.")
                sys.exit(1)
            time.sleep(delay)

    Base.metadata.create_all(bind=engine)
