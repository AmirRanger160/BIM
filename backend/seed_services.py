#!/usr/bin/env python3
"""
Database seeder for creating sample services.

This script creates sample services for BIM and Surveying categories.
"""

import os
import sys
from pathlib import Path
import asyncio

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set environment variables
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/geobiro_db')
os.environ['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
os.environ['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-min-32-chars')

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.models import Service, Base


def seed_services():
    """Create sample services in the database."""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if services already exist
        existing_services = db.query(Service).count()
        if existing_services > 0:
            print(f"✓ {existing_services} خدمات قبلاً وجود دارند")
            db.close()
            return
        
        # Create sample BIM services
        bim_services = [
            Service(
                title_en="3D BIM Modeling",
                title_fa="مدل‌سازی سه‌بعدی BIM",
                description_en="Professional BIM modeling services for architectural and structural design. We create accurate 3D digital representations of buildings for better coordination and planning.",
                description_fa="خدمات حرفه‌ای مدل‌سازی BIM برای طراحی معماری و سازه‌ای. ما نمایش‌های دیجیتالی دقیق سه‌بعدی ساختمان‌ها برای هماهنگی و برنامه‌ریزی بهتر ایجاد می‌کنیم.",
                category="BIM",
                image_url="https://via.placeholder.com/300x250?text=BIM+Modeling",
                software_tools="Revit, ArchiCAD, Tekla Structures"
            ),
            Service(
                title_en="BIM Coordination & Clash Detection",
                title_fa="هماهنگی BIM و تشخیص برخورد",
                description_en="Identify and resolve design conflicts before construction begins. Our clash detection services prevent costly rework and delays on site.",
                description_fa="تشخیص و حل تضادهای طراحی قبل از شروع ساخت‌وساز. خدمات تشخیص برخورد ما از کار دوباره‌ی گران‌قیمت و تاخیر در محل کار جلوگیری می‌کند.",
                category="BIM",
                image_url="https://via.placeholder.com/300x250?text=BIM+Coordination",
                software_tools="Navisworks, Solibri, BIM 360"
            ),
            Service(
                title_en="MEP (Mechanical, Electrical, Plumbing) Design",
                title_fa="طراحی MEP (مکانیکی، الکتریکی، لوله‌کشی)",
                description_en="Comprehensive MEP design and coordination for building systems. Optimize system layouts and ensure proper integration with architectural and structural elements.",
                description_fa="طراحی جامع MEP و هماهنگی سیستم‌های ساختمان. طرح‌های سیستم بهینه و اطمینان از یکپارچگی مناسب با عناصر معماری و سازه‌ای.",
                category="BIM",
                image_url="https://via.placeholder.com/300x250?text=MEP+Design",
                software_tools="Revit MEP, AutoCAD, Trace 700"
            ),
            Service(
                title_en="BIM Documentation & Drawings",
                title_fa="مستندات و نقشه‌های BIM",
                description_en="Generate comprehensive construction documentation from BIM models. Extract accurate 2D drawings, schedules, and specifications from 3D BIM data.",
                description_fa="تولید مستندات ساخت‌وساز جامع از مدل‌های BIM. استخراج نقشه‌های دقیق دو‌بعدی، جداول و مشخصات از داده‌های سه‌بعدی BIM.",
                category="BIM",
                image_url="https://via.placeholder.com/300x250?text=BIM+Documentation",
                software_tools="Revit, AutoCAD, Tekla Structures"
            ),
        ]
        
        # Create sample Surveying services
        surveying_services = [
            Service(
                title_en="Land Surveying & Site Mapping",
                title_fa="نقشه‌برداری زمین و نقشه‌برداری محل",
                description_en="Comprehensive land surveying services using GPS and traditional surveying techniques. We provide accurate boundary determinations and site maps for your projects.",
                description_fa="خدمات جامع نقشه‌برداری زمین با استفاده از GPS و تکنیک‌های سنتی نقشه‌برداری. ما تعیین مرزهای دقیق و نقشه‌های محل برای پروژه‌های شما فراهم می‌کنیم.",
                category="Surveying",
                image_url="https://via.placeholder.com/300x250?text=Land+Surveying",
                software_tools="AutoCAD Civil 3D, Leica Surveying Software, GNSS Equipment"
            ),
            Service(
                title_en="Drone Surveys & Aerial Mapping",
                title_fa="نقشه‌برداری درون‌بین و نقشه‌برداری هوایی",
                description_en="High-resolution aerial surveys using latest drone technology. Get orthophoto maps, 3D point clouds, and terrain models for construction and planning purposes.",
                description_fa="نقشه‌برداری هوایی با وضوح بالا با استفاده از آخرین فناوری درون‌بین. نقشه‌های ارتوفوتو، ابرهای نقاط سه‌بعدی و مدل‌های زمینی برای اهداف ساخت و برنامه‌ریزی دریافت کنید.",
                category="Surveying",
                image_url="https://via.placeholder.com/300x250?text=Drone+Survey",
                software_tools="Pix4D, Drone2Map, DJI Terra"
            ),
            Service(
                title_en="GIS & Geospatial Analysis",
                title_fa="تجزیه و تحلیل GIS و جغرافیایی",
                description_en="Advanced GIS analysis for site assessment, environmental impact studies, and spatial planning. We transform geospatial data into actionable insights.",
                description_fa="تجزیه و تحلیل پیشرفته GIS برای ارزیابی محل، مطالعات تاثیر محیطی و برنامه‌ریزی مکانی. ما داده‌های جغرافیایی را به بینش‌های قابل استفاده تبدیل می‌کنیم.",
                category="Surveying",
                image_url="https://via.placeholder.com/300x250?text=GIS+Analysis",
                software_tools="ArcGIS, QGIS, Global Mapper"
            ),
            Service(
                title_en="As-Built & Deformation Surveys",
                title_fa="نقشه‌برداری وضعیت موجود و تغییر شکل",
                description_en="Precise as-built surveys to document existing conditions. Monitor structural deformation and settlement using advanced surveying techniques.",
                description_fa="نقشه‌برداری دقیق وضعیت موجود برای مستند‌سازی شرایط موجود. نظارت بر تغییر شکل سازه‌ای و نشست با استفاده از تکنیک‌های نقشه‌برداری پیشرفته.",
                category="Surveying",
                image_url="https://via.placeholder.com/300x250?text=As-Built+Survey",
                software_tools="Leica Absolute Arm, FARO, Laser Scanning"
            ),
        ]
        
        # Add all services to database
        all_services = bim_services + surveying_services
        for service in all_services:
            db.add(service)
        
        db.commit()
        print(f"✓ {len(all_services)} خدمات با موفقیت اضافه شدند")
        print(f"  - {len(bim_services)} خدمات BIM")
        print(f"  - {len(surveying_services)} خدمات نقشه‌برداری")
        
    except Exception as e:
        print(f"✗ خطا در اضافه کردن خدمات: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_services()
    print("✓ کار انجام شد!")
