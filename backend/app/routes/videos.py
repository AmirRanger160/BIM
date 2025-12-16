"""
روت‌های مدیریت ویدیوها
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import Video
from app.schemas import Video as VideoSchema, VideoCreate, VideoUpdate

router = APIRouter(prefix="/api/videos", tags=["videos"])


# ============= عمومی (بدون احتیاج به احراز هویت) =============

@router.get("/", response_model=list[VideoSchema])
async def get_videos(
    db: Session = Depends(get_db),
    active_only: bool = Query(True),
    limit: int = Query(10, ge=1, le=100)
):
    """
    دریافت لیست ویدیوها
    - active_only: فقط ویدیوهای فعال
    - limit: تعداد ویدیوها
    """
    query = db.query(Video)
    
    if active_only:
        query = query.filter(Video.active == True)
    
    videos = query.order_by(Video.order, desc(Video.created_at)).limit(limit).all()
    return videos


@router.get("/{video_id}", response_model=VideoSchema)
async def get_video(video_id: int, db: Session = Depends(get_db)):
    """
    دریافت یک ویدیو
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="ویدیو یافت نشد")
    
    # افزایش تعداد بازدید
    video.views += 1
    db.commit()
    
    return video


# ============= ادمین (احتیاج به احراز هویت) =============

@router.post("/", response_model=VideoSchema)
async def create_video(
    video: VideoCreate,
    db: Session = Depends(get_db)
):
    """
    ایجاد ویدیوی جدید
    """
    db_video = Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


@router.put("/{video_id}", response_model=VideoSchema)
async def update_video(
    video_id: int,
    video: VideoUpdate,
    db: Session = Depends(get_db)
):
    """
    بروزرسانی ویدیو
    """
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if not db_video:
        raise HTTPException(status_code=404, detail="ویدیو یافت نشد")
    
    update_data = video.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_video, key, value)
    
    db.commit()
    db.refresh(db_video)
    return db_video


@router.delete("/{video_id}", status_code=200)
async def delete_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    """
    حذف ویدیو
    """
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if not db_video:
        raise HTTPException(status_code=404, detail="ویدیو یافت نشد")
    
    db.delete(db_video)
    db.commit()
    return {"message": "ویدیو حذف شد"}


@router.post("/{video_id}/toggle", response_model=VideoSchema)
async def toggle_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    """
    فعال/غیرفعال کردن ویدیو
    """
    db_video = db.query(Video).filter(Video.id == video_id).first()
    if not db_video:
        raise HTTPException(status_code=404, detail="ویدیو یافت نشد")
    
    db_video.active = not db_video.active
    db.commit()
    db.refresh(db_video)
    return db_video
