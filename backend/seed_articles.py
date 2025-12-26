#!/usr/bin/env python3
"""
Database seeder for creating sample articles.

This script creates sample articles for testing purposes.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Article, Base, engine


def seed_articles():
    """Create sample articles in the database."""
    db = SessionLocal()
    
    try:
        # Check if articles already exist
        existing_articles = db.query(Article).count()
        if existing_articles > 0:
            print(f"✓ {existing_articles} مقالات قبلاً وجود دارند")
            return
        
        # Create sample articles
        sample_articles = [
            Article(
                title_en="Introduction to BIM Technology",
                title_fa="معرفی فناوری BIM",
                slug="introduction-to-bim",
                summary_en="Learn the basics of Building Information Modeling and its impact on modern construction.",
                summary_fa="آشنایی با اصول مدل‌سازی اطلاعات ساختمان و تاثیر آن بر ساخت و ساز مدرن",
                content_en="<p>BIM (Building Information Modeling) is a comprehensive approach to building design, construction, and management. It involves creating a digital representation of a building that contains all relevant information about its geometry, spatial relationships, geographic information, and quantities and properties of building components.</p><p>BIM allows architects, engineers, and contractors to collaborate more effectively, reducing errors and improving efficiency throughout the project lifecycle.</p>",
                content_fa="<p>BIM (مدل‌سازی اطلاعات ساختمان) روشی جامع برای طراحی، ساخت و مدیریت ساختمان است. این روش شامل ایجاد نمایشی دیجیتالی از یک ساختمان است که حاوی تمام اطلاعات مرتبط با هندسه، روابط فضایی، اطلاعات جغرافیایی و خصوصیات اجزای ساختمان است.</p><p>BIM به معماران، مهندسان و پیمانکاران اجازه می‌دهد که به طور موثرتری همکاری کنند و خطاها را کاهش داده و کارایی را در تمام مراحل پروژه بهبود بخشند.</p>",
                category="BIM",
                author="Geobiro Team",
                tags="BIM, technology, construction, modeling",
                is_published=True,
                publish_date=datetime.utcnow() - timedelta(days=7)
            ),
            Article(
                title_en="Surveying: The Foundation of Construction",
                title_fa="نقشه‌برداری: بنیان ساخت و ساز",
                slug="surveying-foundation-construction",
                summary_en="Explore the essential role of surveying in modern construction projects.",
                summary_fa="بررسی نقش حیاتی نقشه‌برداری در پروژه‌های ساخت و ساز مدرن",
                content_en="<p>Surveying is the process of determining positions and distances in the landscape or underwater. It is an essential process for mapping and urban planning, and it is the first step in any construction project.</p><p>Modern surveying techniques include GPS, GIS, LiDAR, and drone technology, which provide accurate and detailed information about the terrain.</p>",
                content_fa="<p>نقشه‌برداری فرایند تعیین موقعیت‌ها و فاصله‌ها در سرزمین یا زیر آب است. این فرایند برای نقشه‌کشی و برنامه‌ریزی شهری ضروری است و اولین مرحله هر پروژه ساخت و ساز است.</p><p>تکنیک‌های نقشه‌برداری مدرن شامل GPS، GIS، LiDAR و فناوری درون‌بین است که اطلاعات دقیق و جزئی‌ای درباره زمین فراهم می‌کند.</p>",
                category="Surveying",
                author="Geobiro Team",
                tags="surveying, GPS, mapping, construction",
                is_published=True,
                publish_date=datetime.utcnow() - timedelta(days=5)
            ),
            Article(
                title_en="Latest Updates in Geospatial Technology",
                title_fa="آخرین به‌روزرسانی‌های فناوری جغرافیایی",
                slug="geospatial-technology-updates",
                summary_en="Stay informed about the latest developments in geospatial technology.",
                summary_fa="از آخرین پیشرفت‌های فناوری جغرافیایی آگاه بمانید",
                content_en="<p>Geospatial technology is rapidly evolving with new tools and methodologies emerging every year. The integration of AI and machine learning with geospatial data is opening new possibilities for analysis and decision-making.</p><p>Organizations are increasingly adopting cloud-based GIS solutions for better scalability and collaboration.</p>",
                content_fa="<p>فناوری جغرافیایی به سرعت در حال تکامل است و ابزارها و روش‌های جدید هر سال ظاهر می‌شوند. ادغام هوش مصنوعی و یادگیری ماشین با داده‌های جغرافیایی امکانات جدیدی برای تجزیه و تحلیل و تصمیم‌گیری باز می‌کند.</p><p>سازمان‌ها به طور فزاینده‌ای راه‌حل‌های GIS مبتنی بر ابر را برای مقیاس‌پذیری و همکاری بهتر می‌پذیرند.</p>",
                category="Technology",
                author="Geobiro Team",
                tags="geospatial, AI, technology, cloud",
                is_published=True,
                publish_date=datetime.utcnow() - timedelta(days=3)
            ),
            Article(
                title_en="Success Stories: BIM in Large-Scale Projects",
                title_fa="داستان‌های موفقیت: BIM در پروژه‌های بزرگ",
                slug="bim-success-stories",
                summary_en="Learn how BIM has revolutionized major construction projects around the world.",
                summary_fa="بیاموزید چگونه BIM پروژه‌های ساخت و ساز بزرگ در سراسر جهان را متحول کرده است",
                content_en="<p>Major infrastructure projects like bridges, airports, and skyscrapers have successfully implemented BIM to improve coordination and reduce costs.</p><p>Case studies show that BIM adoption can reduce project duration by 20-30% and prevent costly rework.</p>",
                content_fa="<p>پروژه‌های زیربنایی بزرگ مثل پل‌ها، فرودگاه‌ها و آسمان‌خراش‌ها با موفقیت BIM را پیاده‌سازی کرده‌اند تا هماهنگی را بهبود بخشند و هزینه‌ها را کاهش دهند.</p><p>مطالعات موردی نشان می‌دهد که پذیرش BIM می‌تواند مدت پروژه را 20-30% کاهش دهد و از کار دوباره مجددی گران‌قیمت جلوگیری کند.</p>",
                category="BIM",
                author="Geobiro Team",
                tags="BIM, projects, infrastructure, success",
                is_published=True,
                publish_date=datetime.utcnow() - timedelta(days=1)
            ),
            Article(
                title_en="Drone Technology in Land Surveying",
                title_fa="فناوری درون‌بین در نقشه‌برداری زمین",
                slug="drone-surveying-technology",
                summary_en="Discover how drones are transforming surveying and mapping practices.",
                summary_fa="کشف کنید چگونه درون‌بین‌ها عملیات نقشه‌برداری را تغییر می‌دهند",
                content_en="<p>Unmanned Aerial Vehicles (UAVs) or drones have become indispensable tools in modern surveying. They provide high-resolution imagery and data collection capabilities at a fraction of the cost of traditional methods.</p><p>Drone-based surveying is faster, safer, and more accurate than traditional ground-based surveying.</p>",
                content_fa="<p>خودروهای بدون سرنشین (UAV) یا درون‌بین‌ها به ابزارهای ضروری در نقشه‌برداری مدرن تبدیل شده‌اند. آنها تصاویر با وضوح بالا و قابلیت جمع‌آوری داده در کسری از هزینه روش‌های سنتی فراهم می‌کنند.</p><p>نقشه‌برداری مبتنی بر درون‌بین سریع‌تر، ایمن‌تر و دقیق‌تر از نقشه‌برداری سنتی است.</p>",
                category="Surveying",
                author="Geobiro Team",
                tags="drone, surveying, UAV, technology",
                is_published=True,
                publish_date=datetime.utcnow()
            )
        ]
        
        db.add_all(sample_articles)
        db.commit()
        
        print(f"✓ {len(sample_articles)} مقالات با موفقیت اضافه شد")
        for article in sample_articles:
            print(f"  - {article.title_fa} ({article.slug})")
        
    except Exception as e:
        print(f"✗ خطا در اضافه کردن مقالات: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_articles()
