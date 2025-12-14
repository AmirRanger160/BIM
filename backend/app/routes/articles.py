from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/articles", tags=["Articles"])


@router.get("", response_model=dict)
def get_articles(
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "latest",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """دریافت لیست مقالات با فیلتر و pagination"""
    query = db.query(models.Article)
    
    # فیلتر بر اساس دسته‌بندی
    if category and category != "همه":
        query = query.filter(models.Article.category == category)
    
    # جستجو در عنوان و excerpt
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.Article.title.ilike(search_filter)) |
            (models.Article.excerpt.ilike(search_filter))
        )
    
    # مرتب‌سازی
    if sort == "popular":
        query = query.order_by(models.Article.views.desc())
    elif sort == "trending":
        query = query.order_by(models.Article.featured.desc(), models.Article.views.desc())
    else:  # latest
        query = query.order_by(models.Article.created_at.desc())
    
    # محاسبه pagination
    total = query.count()
    total_pages = math.ceil(total / limit)
    offset = (page - 1) * limit
    
    articles = query.offset(offset).limit(limit).all()
    
    # تبدیل به dict برای serialization
    articles_data = [schemas.Article.from_orm(article) for article in articles]
    
    return {
        "data": articles_data,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": total_pages
    }


@router.get("/{article_id}", response_model=dict)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """دریافت یک مقاله با ID"""
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="مقاله یافت نشد")
    
    # افزایش تعداد بازدید
    article.views += 1
    db.commit()
    db.refresh(article)
    
    return {"data": schemas.Article.from_orm(article)}


@router.post("", response_model=dict, status_code=201)
def create_article(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ایجاد مقاله جدید (فقط ادمین)"""
    db_article = models.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    return {
        "data": schemas.Article.from_orm(db_article),
        "message": "مقاله با موفقیت ایجاد شد"
    }


@router.put("/{article_id}", response_model=dict)
def update_article(
    article_id: int,
    article: schemas.ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """بروزرسانی مقاله (فقط ادمین)"""
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    
    if not db_article:
        raise HTTPException(status_code=404, detail="مقاله یافت نشد")
    
    # بروزرسانی فیلدها
    update_data = article.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_article, field, value)
    
    db.commit()
    db.refresh(db_article)
    
    return {
        "data": schemas.Article.from_orm(db_article),
        "message": "مقاله با موفقیت بروزرسانی شد"
    }


@router.delete("/{article_id}", response_model=dict)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """حذف مقاله (فقط ادمین)"""
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    
    if not db_article:
        raise HTTPException(status_code=404, detail="مقاله یافت نشد")
    
    db.delete(db_article)
    db.commit()
    
    return {
        "success": True,
        "message": "مقاله با موفقیت حذف شد"
    }


@router.get("/categories/list", response_model=dict)
def get_categories(db: Session = Depends(get_db)):
    """دریافت لیست دسته‌بندی‌های مقالات"""
    categories = db.query(models.Article.category).distinct().all()
    category_list = ["همه"] + [cat[0] for cat in categories]
    
    return {
        "data": category_list
    }
