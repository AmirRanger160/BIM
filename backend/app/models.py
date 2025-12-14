from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.database import Base


class Article(Base):
    """مدل مقالات"""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    excerpt = Column(Text, nullable=False)
    full_content = Column(Text, nullable=True)
    category = Column(String(100), nullable=False, index=True)
    icon = Column(String(10), default="📝")
    gradient = Column(String(255))
    # تصاویر
    image = Column(String(500), nullable=True)  # تصویر شاخص
    slider_id = Column(Integer, nullable=True)  # اسلایدر (بجای images)
    author = Column(String(100), nullable=False)
    author_avatar = Column(String(10))
    author_role = Column(String(100))
    views = Column(Integer, default=0)
    read_time = Column(String(50))
    featured = Column(Boolean, default=False)
    tags = Column(JSON)  # لیست تگ‌ها
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class GalleryItem(Base):
    """مدل آیتم‌های گالری"""
    __tablename__ = "gallery_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(10), default="🎨")
    gradient = Column(String(255))
    # تصاویر
    image = Column(String(500), nullable=True)  # تصویر شاخص
    slider_id = Column(Integer, nullable=True)  # اسلایدر (بجای images)
    category = Column(String(100), nullable=False, index=True)
    category_color = Column(String(50))
    date = Column(String(50))
    duration = Column(String(50))
    views = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    technologies = Column(JSON)  # لیست تکنولوژی‌ها
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Testimonial(Base):
    """مدل نظرات مشتریان"""
    __tablename__ = "testimonials"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    avatar = Column(String(10))
    text = Column(Text, nullable=False)
    rating = Column(Integer, default=5)
    date = Column(String(50))
    project = Column(String(255))
    approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Certificate(Base):
    """مدل گواهینامه‌ها"""
    __tablename__ = "certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    issuer = Column(String(255), nullable=False)
    date = Column(String(50))
    icon = Column(String(10))
    color = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Statistic(Base):
    """مدل آمار سایت"""
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), nullable=False)
    label = Column(String(100), nullable=False)
    icon = Column(String(10))
    order = Column(Integer, default=0)


class Contact(Base):
    """مدل پیام‌های تماس"""
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Newsletter(Base):
    """مدل خبرنامه"""
    __tablename__ = "newsletters"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Slider(Base):
    """مدل اسلایدرها (مجموعه تصاویر برای گالری/مقالات)"""
    __tablename__ = "sliders"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)  # نام slider
    description = Column(Text, nullable=True)
    images = Column(JSON, nullable=True, default=[])  # لیست URL های تصاویر
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base):
    """مدل کاربران (برای ادمین)"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
