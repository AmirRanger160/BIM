from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import math

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/gallery", tags=["Gallery"])


@router.get("", response_model=dict)
def get_gallery_items(
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """دریافت لیست آیتم‌های گالری"""
    query = db.query(models.GalleryItem)
    
    # فیلتر دسته‌بندی
    if category and category != "همه":
        query = query.filter(models.GalleryItem.category == category)
    
    # جستجو
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.GalleryItem.title.ilike(search_filter)) |
            (models.GalleryItem.description.ilike(search_filter))
        )
    
    # مرتب‌سازی بر اساس تاریخ
    query = query.order_by(models.GalleryItem.created_at.desc())
    
    # Pagination
    total = query.count()
    total_pages = math.ceil(total / limit)
    offset = (page - 1) * limit
    
    items = query.offset(offset).limit(limit).all()
    
    items_data = [schemas.GalleryItem.from_orm(item) for item in items]
    
    return {
        "data": items_data,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": total_pages
    }


@router.get("/{item_id}", response_model=dict)
def get_gallery_item(item_id: int, db: Session = Depends(get_db)):
    """دریافت یک آیتم گالری"""
    item = db.query(models.GalleryItem).filter(models.GalleryItem.id == item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="آیتم یافت نشد")
    
    # افزایش بازدید
    item.views += 1
    db.commit()
    db.refresh(item)
    
    return {"data": schemas.GalleryItem.from_orm(item)}


@router.post("", response_model=dict, status_code=201)
def create_gallery_item(
    item: schemas.GalleryItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ایجاد آیتم گالری جدید (فقط ادمین)"""
    db_item = models.GalleryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return {
        "data": schemas.GalleryItem.from_orm(db_item),
        "message": "آیتم با موفقیت ایجاد شد"
    }


@router.put("/{item_id}", response_model=dict)
def update_gallery_item(
    item_id: int,
    item: schemas.GalleryItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """بروزرسانی آیتم گالری (فقط ادمین)"""
    db_item = db.query(models.GalleryItem).filter(models.GalleryItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="آیتم یافت نشد")
    
    update_data = item.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    
    return {
        "data": schemas.GalleryItem.from_orm(db_item),
        "message": "آیتم با موفقیت بروزرسانی شد"
    }


@router.delete("/{item_id}", response_model=dict)
def delete_gallery_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """حذف آیتم گالری (فقط ادمین)"""
    db_item = db.query(models.GalleryItem).filter(models.GalleryItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="آیتم یافت نشد")
    
    db.delete(db_item)
    db.commit()
    
    return {
        "success": True,
        "message": "آیتم با موفقیت حذف شد"
    }


@router.get("/categories/list", response_model=dict)
def get_categories(db: Session = Depends(get_db)):
    """دریافت لیست دسته‌بندی‌ها"""
    categories = db.query(models.GalleryItem.category).distinct().all()
    category_list = ["همه"] + [cat[0] for cat in categories]
    
    return {
        "data": category_list
    }
