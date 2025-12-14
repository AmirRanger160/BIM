from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from pathlib import Path

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# ==================== مقالات ====================

@router.get("/articles", response_model=List[schemas.Article])
def get_all_articles_admin(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """دریافت همه مقالات (ادمین)"""
    articles = db.query(models.Article).offset(skip).limit(limit).all()
    return articles


@router.post("/articles", response_model=schemas.Article, status_code=201)
def create_article_admin(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ایجاد مقاله جدید (ادمین)"""
    db_article = models.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.put("/articles/{article_id}", response_model=schemas.Article)
def update_article_admin(
    article_id: int,
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ویرایش مقاله (ادمین)"""
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="مقاله یافت نشد")
    
    for key, value in article.dict().items():
        setattr(db_article, key, value)
    
    db.commit()
    db.refresh(db_article)
    return db_article


@router.delete("/articles/{article_id}")
def delete_article_admin(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """حذف مقاله (ادمین)"""
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="مقاله یافت نشد")
    
    db.delete(db_article)
    db.commit()
    return {"success": True, "message": "مقاله با موفقیت حذف شد"}


# ==================== گالری ====================

@router.get("/gallery", response_model=List[schemas.GalleryItem])
def get_all_gallery_admin(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """دریافت همه آیتم‌های گالری (ادمین)"""
    items = db.query(models.GalleryItem).offset(skip).limit(limit).all()
    return items


@router.post("/gallery", response_model=schemas.GalleryItem, status_code=201)
def create_gallery_admin(
    item: schemas.GalleryItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ایجاد آیتم گالری جدید (ادمین)"""
    db_item = models.GalleryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/gallery/{item_id}", response_model=schemas.GalleryItem)
def update_gallery_admin(
    item_id: int,
    item: schemas.GalleryItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ویرایش آیتم گالری (ادمین)"""
    db_item = db.query(models.GalleryItem).filter(models.GalleryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="آیتم یافت نشد")
    
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/gallery/{item_id}")
def delete_gallery_admin(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """حذف آیتم گالری (ادمین)"""
    db_item = db.query(models.GalleryItem).filter(models.GalleryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="آیتم یافت نشد")
    
    db.delete(db_item)
    db.commit()
    return {"success": True, "message": "آیتم با موفقیت حذف شد"}


# ==================== نظرات ====================

@router.get("/testimonials", response_model=List[schemas.Testimonial])
def get_all_testimonials_admin(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """دریافت همه نظرات (ادمین)"""
    testimonials = db.query(models.Testimonial).offset(skip).limit(limit).all()
    return testimonials


@router.post("/testimonials", response_model=schemas.Testimonial, status_code=201)
def create_testimonial_admin(
    testimonial: schemas.TestimonialCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ایجاد نظر جدید (ادمین)"""
    db_testimonial = models.Testimonial(**testimonial.dict())
    db.add(db_testimonial)
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial


@router.put("/testimonials/{testimonial_id}", response_model=schemas.Testimonial)
def update_testimonial_admin(
    testimonial_id: int,
    testimonial: schemas.TestimonialCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ویرایش نظر (ادمین)"""
    db_testimonial = db.query(models.Testimonial).filter(models.Testimonial.id == testimonial_id).first()
    if not db_testimonial:
        raise HTTPException(status_code=404, detail="نظر یافت نشد")
    
    for key, value in testimonial.dict().items():
        setattr(db_testimonial, key, value)
    
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial


@router.delete("/testimonials/{testimonial_id}")
def delete_testimonial_admin(
    testimonial_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """حذف نظر (ادمین)"""
    db_testimonial = db.query(models.Testimonial).filter(models.Testimonial.id == testimonial_id).first()
    if not db_testimonial:
        raise HTTPException(status_code=404, detail="نظر یافت نشد")
    
    db.delete(db_testimonial)
    db.commit()
    return {"success": True, "message": "نظر با موفقیت حذف شد"}


@router.patch("/testimonials/{testimonial_id}/approve")
def approve_testimonial_admin(
    testimonial_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """تایید نظر (ادمین)"""
    db_testimonial = db.query(models.Testimonial).filter(models.Testimonial.id == testimonial_id).first()
    if not db_testimonial:
        raise HTTPException(status_code=404, detail="نظر یافت نشد")
    
    db_testimonial.approved = True
    db.commit()
    return {"success": True, "message": "نظر تایید شد"}


# ==================== پیام‌های تماس ====================

@router.get("/contacts")
def get_all_contacts_admin(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """دریافت همه پیام‌های تماس (ادمین)"""
    contacts = db.query(models.Contact).offset(skip).limit(limit).all()
    return contacts


@router.patch("/contacts/{contact_id}/read")
def mark_contact_read_admin(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """علامت‌گذاری پیام به عنوان خوانده شده (ادمین)"""
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="پیام یافت نشد")
    
    db_contact.read = True
    db.commit()
    return {"success": True, "message": "پیام به عنوان خوانده شده علامت‌گذاری شد"}


@router.delete("/contacts/{contact_id}")
def delete_contact_admin(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """حذف پیام تماس (ادمین)"""
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="پیام یافت نشد")
    
    db.delete(db_contact)
    db.commit()
    return {"success": True, "message": "پیام با موفقیت حذف شد"}


# ==================== آمار داشبورد ====================

# ==================== اسلایدرها ====================

@router.get("/sliders", response_model=List[schemas.Slider])
def get_all_sliders_admin(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """دریافت همه اسلایدرها (ادمین)"""
    sliders = db.query(models.Slider).offset(skip).limit(limit).all()
    return sliders


@router.post("/sliders", response_model=schemas.Slider, status_code=201)
def create_slider_admin(
    slider: schemas.SliderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ایجاد اسلایدر جدید (ادمین)"""
    db_slider = models.Slider(**slider.dict())
    db.add(db_slider)
    db.commit()
    db.refresh(db_slider)
    return db_slider


@router.put("/sliders/{slider_id}", response_model=schemas.Slider)
def update_slider_admin(
    slider_id: int,
    slider: schemas.SliderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ویرایش اسلایدر (ادمین)"""
    db_slider = db.query(models.Slider).filter(models.Slider.id == slider_id).first()
    if not db_slider:
        raise HTTPException(status_code=404, detail="اسلایدر یافت نشد")
    
    for key, value in slider.dict().items():
        setattr(db_slider, key, value)
    
    db.commit()
    db.refresh(db_slider)
    return db_slider


@router.delete("/sliders/{slider_id}")
def delete_slider_admin(
    slider_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """حذف اسلایدر (ادمین)"""
    db_slider = db.query(models.Slider).filter(models.Slider.id == slider_id).first()
    if not db_slider:
        raise HTTPException(status_code=404, detail="اسلایدر یافت نشد")
    
    db.delete(db_slider)
    db.commit()
    return {"success": True, "message": "اسلایدر با موفقیت حذف شد"}


@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """دریافت آمار داشبورد (ادمین)"""
    articles_count = db.query(models.Article).count()
    gallery_count = db.query(models.GalleryItem).count()
    testimonials_count = db.query(models.Testimonial).count()
    contacts_count = db.query(models.Contact).count()
    sliders_count = db.query(models.Slider).count()
    unread_contacts = db.query(models.Contact).filter(models.Contact.read == False).count()
    pending_testimonials = db.query(models.Testimonial).filter(models.Testimonial.approved == False).count()
    
    return {
        "articles": articles_count,
        "gallery": gallery_count,
        "testimonials": testimonials_count,
        "contacts": contacts_count,
        "sliders": sliders_count,
        "unread_contacts": unread_contacts,
        "pending_testimonials": pending_testimonials
    }
