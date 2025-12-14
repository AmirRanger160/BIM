from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api", tags=["Other"])


# ============= TESTIMONIALS =============

@router.get("/testimonials", response_model=dict)
def get_testimonials(db: Session = Depends(get_db)):
    """دریافت نظرات تایید شده"""
    testimonials = db.query(models.Testimonial)\
        .filter(models.Testimonial.approved == True)\
        .order_by(models.Testimonial.created_at.desc())\
        .all()
    
    testimonials_data = [schemas.Testimonial.from_orm(t) for t in testimonials]
    return {"data": testimonials_data}


@router.post("/testimonials", response_model=dict, status_code=201)
def create_testimonial(
    testimonial: schemas.TestimonialCreate,
    db: Session = Depends(get_db)
):
    """ثبت نظر جدید (نیاز به تایید ادمین دارد)"""
    db_testimonial = models.Testimonial(
        **testimonial.dict(),
        approved=False  # باید توسط ادمین تایید شود
    )
    db.add(db_testimonial)
    db.commit()
    db.refresh(db_testimonial)
    
    return {
        "data": schemas.Testimonial.from_orm(db_testimonial),
        "message": "نظر شما ثبت شد و پس از بررسی منتشر خواهد شد"
    }


@router.put("/testimonials/{testimonial_id}/approve", response_model=dict)
def approve_testimonial(
    testimonial_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """تایید نظر (فقط ادمین)"""
    testimonial = db.query(models.Testimonial).filter(
        models.Testimonial.id == testimonial_id
    ).first()
    
    if not testimonial:
        raise HTTPException(status_code=404, detail="نظر یافت نشد")
    
    testimonial.approved = True
    db.commit()
    
    return {
        "success": True,
        "message": "نظر با موفقیت تایید شد"
    }


# ============= CERTIFICATES =============

@router.get("/certificates", response_model=dict)
def get_certificates(db: Session = Depends(get_db)):
    """دریافت گواهینامه‌ها"""
    certificates = db.query(models.Certificate)\
        .order_by(models.Certificate.created_at.desc())\
        .all()
    
    certificates_data = [schemas.Certificate.from_orm(c) for c in certificates]
    return {"data": certificates_data}


@router.post("/certificates", response_model=dict, status_code=201)
def create_certificate(
    certificate: schemas.CertificateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ایجاد گواهینامه جدید (فقط ادمین)"""
    db_certificate = models.Certificate(**certificate.dict())
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    
    return {
        "data": schemas.Certificate.from_orm(db_certificate),
        "message": "گواهینامه با موفقیت اضافه شد"
    }


# ============= STATISTICS =============

@router.get("/statistics", response_model=dict)
def get_statistics(db: Session = Depends(get_db)):
    """دریافت آمار سایت"""
    statistics = db.query(models.Statistic)\
        .order_by(models.Statistic.order)\
        .all()
    
    statistics_data = [schemas.Statistic.from_orm(s) for s in statistics]
    return {"data": statistics_data}


@router.post("/statistics", response_model=dict, status_code=201)
def create_statistic(
    statistic: schemas.StatisticCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """ایجاد آمار جدید (فقط ادمین)"""
    db_statistic = models.Statistic(**statistic.dict())
    db.add(db_statistic)
    db.commit()
    db.refresh(db_statistic)
    
    return {
        "data": schemas.Statistic.from_orm(db_statistic),
        "message": "آمار با موفقیت اضافه شد"
    }


@router.put("/statistics/{stat_id}", response_model=dict)
def update_statistic(
    stat_id: int,
    number: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """بروزرسانی آمار (فقط ادمین)"""
    statistic = db.query(models.Statistic).filter(models.Statistic.id == stat_id).first()
    
    if not statistic:
        raise HTTPException(status_code=404, detail="آمار یافت نشد")
    
    statistic.number = number
    db.commit()
    db.refresh(statistic)
    
    return {
        "data": schemas.Statistic.from_orm(statistic),
        "message": "آمار بروزرسانی شد"
    }


# ============= CONTACT =============

@router.post("/contact", response_model=dict)
def send_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db)
):
    """ارسال فرم تماس"""
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    # اینجا می‌توانید ایمیل ارسال کنید
    
    return {
        "success": True,
        "message": "پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت."
    }


@router.get("/contact/messages", response_model=dict)
def get_messages(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """دریافت پیام‌ها (فقط ادمین)"""
    messages = db.query(models.Contact)\
        .order_by(models.Contact.created_at.desc())\
        .all()
    
    messages_data = [schemas.Contact.from_orm(m) for m in messages]
    return {"data": messages_data}


@router.put("/contact/{message_id}/read", response_model=dict)
def mark_message_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """علامت‌گذاری پیام به عنوان خوانده شده (فقط ادمین)"""
    message = db.query(models.Contact).filter(models.Contact.id == message_id).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="پیام یافت نشد")
    
    message.read = True
    db.commit()
    
    return {
        "success": True,
        "message": "پیام به عنوان خوانده شده علامت‌گذاری شد"
    }


# ============= NEWSLETTER =============

@router.post("/newsletter/subscribe", response_model=dict)
def subscribe_newsletter(
    email_data: schemas.NewsletterCreate,
    db: Session = Depends(get_db)
):
    """ثبت‌نام در خبرنامه"""
    # بررسی وجود ایمیل
    existing = db.query(models.Newsletter).filter(
        models.Newsletter.email == email_data.email
    ).first()
    
    if existing:
        if existing.active:
            return {
                "success": True,
                "message": "این ایمیل قبلا ثبت شده است"
            }
        else:
            # فعال کردن مجدد
            existing.active = True
            db.commit()
            return {
                "success": True,
                "message": "اشتراک شما مجددا فعال شد"
            }
    
    # ثبت ایمیل جدید
    db_newsletter = models.Newsletter(**email_data.dict())
    db.add(db_newsletter)
    db.commit()
    
    return {
        "success": True,
        "message": "ایمیل شما با موفقیت در خبرنامه ثبت شد"
    }


@router.get("/newsletter/subscribers", response_model=dict)
def get_subscribers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """دریافت لیست مشترکین (فقط ادمین)"""
    subscribers = db.query(models.Newsletter)\
        .filter(models.Newsletter.active == True)\
        .order_by(models.Newsletter.created_at.desc())\
        .all()
    
    subscribers_data = [schemas.Newsletter.from_orm(s) for s in subscribers]
    return {
        "data": subscribers_data,
        "total": len(subscribers_data)
    }
