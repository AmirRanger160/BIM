from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Comment, User
from app.schemas import CommentCreate, Comment as CommentSchema, CommentUpdate
from app.auth import get_current_user

router = APIRouter(prefix="/api/comments", tags=["Comments"])


@router.get("/", response_model=List[CommentSchema])
def get_comments(
    content_type: Optional[str] = Query(None, pattern="^(article|project)$"),
    content_id: Optional[int] = None,
    approved_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """دریافت لیست نظرات با فیلتر"""
    query = db.query(Comment)
    
    # فیلتر نوع محتوا
    if content_type:
        query = query.filter(Comment.content_type == content_type)
    
    # فیلتر شناسه محتوا
    if content_id:
        query = query.filter(Comment.content_id == content_id)
    
    # فیلتر نظرات تایید شده
    if approved_only:
        query = query.filter(Comment.approved == True)
    
    # مرتب‌سازی بر اساس تاریخ (جدیدترین اول)
    query = query.order_by(Comment.created_at.desc())
    
    return query.offset(skip).limit(limit).all()


@router.get("/{comment_id}", response_model=CommentSchema)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """دریافت یک نظر با شناسه"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="نظر یافت نشد")
    return comment


@router.post("/", response_model=CommentSchema, status_code=201)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    """ایجاد نظر جدید (نیاز به تایید ادمین)"""
    
    # اعتبارسنجی نوع محتوا
    if comment.content_type not in ["article", "project"]:
        raise HTTPException(
            status_code=400, 
            detail="نوع محتوا باید article یا project باشد"
        )
    
    # اعتبارسنجی امتیاز
    if comment.rating < 1 or comment.rating > 5:
        raise HTTPException(
            status_code=400,
            detail="امتیاز باید بین 1 تا 5 باشد"
        )
    
    # ایجاد نظر جدید (approved=False به صورت پیش‌فرض)
    db_comment = Comment(
        name=comment.name,
        email=comment.email,
        content=comment.content,
        rating=comment.rating,
        content_type=comment.content_type,
        content_id=comment.content_id,
        approved=False  # نیاز به تایید ادمین
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return db_comment


@router.put("/{comment_id}/approve", response_model=CommentSchema)
def approve_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """تایید یا رد نظر (فقط ادمین)"""
    
    # بررسی دسترسی ادمین
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="دسترسی ممنوع")
    
    # پیدا کردن نظر
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="نظر یافت نشد")
    
    # تغییر وضعیت تایید
    comment.approved = not comment.approved
    comment.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(comment)
    
    return comment


@router.put("/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ویرایش نظر (فقط ادمین)"""
    
    # بررسی دسترسی ادمین
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="دسترسی ممنوع")
    
    # پیدا کردن نظر
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="نظر یافت نشد")
    
    # بروزرسانی فیلدهای ارائه شده
    if comment_update.name is not None:
        comment.name = comment_update.name
    if comment_update.email is not None:
        comment.email = comment_update.email
    if comment_update.content is not None:
        comment.content = comment_update.content
    if comment_update.rating is not None:
        if comment_update.rating < 1 or comment_update.rating > 5:
            raise HTTPException(
                status_code=400,
                detail="امتیاز باید بین 1 تا 5 باشد"
            )
        comment.rating = comment_update.rating
    if comment_update.approved is not None:
        comment.approved = comment_update.approved
    
    comment.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(comment)
    
    return comment


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """حذف نظر (فقط ادمین)"""
    
    # بررسی دسترسی ادمین
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="دسترسی ممنوع")
    
    # پیدا کردن نظر
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="نظر یافت نشد")
    
    db.delete(comment)
    db.commit()
    
    return {"success": True, "message": "نظر با موفقیت حذف شد"}


@router.get("/stats/summary")
def get_comment_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """دریافت آمار نظرات (فقط ادمین)"""
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="دسترسی ممنوع")
    
    total_comments = db.query(Comment).count()
    approved_comments = db.query(Comment).filter(Comment.approved == True).count()
    pending_comments = db.query(Comment).filter(Comment.approved == False).count()
    
    # میانگین امتیاز
    avg_rating = db.query(Comment).filter(Comment.approved == True).with_entities(
        db.func.avg(Comment.rating)
    ).scalar() or 0
    
    return {
        "total": total_comments,
        "approved": approved_comments,
        "pending": pending_comments,
        "average_rating": round(float(avg_rating), 2)
    }
