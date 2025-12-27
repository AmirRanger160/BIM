#!/bin/bash

# Get admin token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo "Token: $TOKEN"

# Function to add a service
add_service() {
  local title_en="$1"
  local title_fa="$2"
  local description_en="$3"
  local description_fa="$4"
  local category="$5"
  local image_url="$6"
  local software_tools="$7"

  curl -s -X POST http://localhost:8000/api/services \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"title\": \"$title_en\",
      \"title_en\": \"$title_en\",
      \"title_fa\": \"$title_fa\",
      \"description\": \"$description_en\",
      \"description_en\": \"$description_en\",
      \"description_fa\": \"$description_fa\",
      \"category\": \"$category\",
      \"image_url\": \"$image_url\",
      \"software_tools\": \"$software_tools\"
    }"
  
  echo ""
}

# Add BIM services
echo "Adding BIM Services..."

add_service \
  "3D BIM Modeling" \
  "مدل‌سازی سه‌بعدی BIM" \
  "Professional BIM modeling services for architectural and structural design. We create accurate 3D digital representations of buildings for better coordination and planning." \
  "خدمات حرفه‌ای مدل‌سازی BIM برای طراحی معماری و سازه‌ای. ما نمایش‌های دیجیتالی دقیق سه‌بعدی ساختمان‌ها برای هماهنگی و برنامه‌ریزی بهتر ایجاد می‌کنیم." \
  "BIM" \
  "https://via.placeholder.com/300x250?text=BIM+Modeling" \
  "Revit, ArchiCAD, Tekla Structures"

add_service \
  "BIM Coordination & Clash Detection" \
  "هماهنگی BIM و تشخیص برخورد" \
  "Identify and resolve design conflicts before construction begins. Our clash detection services prevent costly rework and delays on site." \
  "تشخیص و حل تضادهای طراحی قبل از شروع ساخت‌وساز. خدمات تشخیص برخورد ما از کار دوباره‌ی گران‌قیمت و تاخیر در محل کار جلوگیری می‌کند." \
  "BIM" \
  "https://via.placeholder.com/300x250?text=BIM+Coordination" \
  "Navisworks, Solibri, BIM 360"

add_service \
  "MEP (Mechanical, Electrical, Plumbing) Design" \
  "طراحی MEP (مکانیکی، الکتریکی، لوله‌کشی)" \
  "Comprehensive MEP design and coordination for building systems. Optimize system layouts and ensure proper integration with architectural and structural elements." \
  "طراحی جامع MEP و هماهنگی سیستم‌های ساختمان. طرح‌های سیستم بهینه و اطمینان از یکپارچگی مناسب با عناصر معماری و سازه‌ای." \
  "BIM" \
  "https://via.placeholder.com/300x250?text=MEP+Design" \
  "Revit MEP, AutoCAD, Trace 700"

add_service \
  "BIM Documentation & Drawings" \
  "مستندات و نقشه‌های BIM" \
  "Generate comprehensive construction documentation from BIM models. Extract accurate 2D drawings, schedules, and specifications from 3D BIM data." \
  "تولید مستندات ساخت‌وساز جامع از مدل‌های BIM. استخراج نقشه‌های دقیق دو‌بعدی، جداول و مشخصات از داده‌های سه‌بعدی BIM." \
  "BIM" \
  "https://via.placeholder.com/300x250?text=BIM+Documentation" \
  "Revit, AutoCAD, Tekla Structures"

# Add Surveying services
echo "Adding Surveying Services..."

add_service \
  "Land Surveying & Site Mapping" \
  "نقشه‌برداری زمین و نقشه‌برداری محل" \
  "Comprehensive land surveying services using GPS and traditional surveying techniques. We provide accurate boundary determinations and site maps for your projects." \
  "خدمات جامع نقشه‌برداری زمین با استفاده از GPS و تکنیک‌های سنتی نقشه‌برداری. ما تعیین مرزهای دقیق و نقشه‌های محل برای پروژه‌های شما فراهم می‌کنیم." \
  "Surveying" \
  "https://via.placeholder.com/300x250?text=Land+Surveying" \
  "AutoCAD Civil 3D, Leica Surveying Software, GNSS Equipment"

add_service \
  "Drone Surveys & Aerial Mapping" \
  "نقشه‌برداری درون‌بین و نقشه‌برداری هوایی" \
  "High-resolution aerial surveys using latest drone technology. Get orthophoto maps, 3D point clouds, and terrain models for construction and planning purposes." \
  "نقشه‌برداری هوایی با وضوح بالا با استفاده از آخرین فناوری درون‌بین. نقشه‌های ارتوفوتو، ابرهای نقاط سه‌بعدی و مدل‌های زمینی برای اهداف ساخت و برنامه‌ریزی دریافت کنید." \
  "Surveying" \
  "https://via.placeholder.com/300x250?text=Drone+Survey" \
  "Pix4D, Drone2Map, DJI Terra"

add_service \
  "GIS & Geospatial Analysis" \
  "تجزیه و تحلیل GIS و جغرافیایی" \
  "Advanced GIS analysis for site assessment, environmental impact studies, and spatial planning. We transform geospatial data into actionable insights." \
  "تجزیه و تحلیل پیشرفته GIS برای ارزیابی محل، مطالعات تاثیر محیطی و برنامه‌ریزی مکانی. ما داده‌های جغرافیایی را به بینش‌های قابل استفاده تبدیل می‌کنیم." \
  "Surveying" \
  "https://via.placeholder.com/300x250?text=GIS+Analysis" \
  "ArcGIS, QGIS, Global Mapper"

add_service \
  "As-Built & Deformation Surveys" \
  "نقشه‌برداری وضعیت موجود و تغییر شکل" \
  "Precise as-built surveys to document existing conditions. Monitor structural deformation and settlement using advanced surveying techniques." \
  "نقشه‌برداری دقیق وضعیت موجود برای مستند‌سازی شرایط موجود. نظارت بر تغییر شکل سازه‌ای و نشست با استفاده از تکنیک‌های نقشه‌برداری پیشرفته." \
  "Surveying" \
  "https://via.placeholder.com/300x250?text=As-Built+Survey" \
  "Leica Absolute Arm, FARO, Laser Scanning"

echo "✓ All services added successfully!"
