from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import ContactSubmission, CompanyInfo, Statistics
from app.schemas.schemas import (
    ContactSubmissionCreate, ContactSubmissionResponse, ContactSubmissionDetail,
    CompanyInfoCreate, CompanyInfoUpdate, CompanyInfoResponse,
    StatisticsUpdate, StatisticsResponse
)
from app.core.security import require_admin
from app.services.email_service import send_contact_notification, send_contact_confirmation
from app.cache import (
    get_cached, set_cache, delete_cache,
    CACHE_KEYS, CACHE_TTL
)

router = APIRouter(tags=["Contact & Company"])


# ============ Contact Form Endpoints ============

@router.post("/contact", response_model=ContactSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact_form(
    contact_data: ContactSubmissionCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Submit a contact form (public endpoint)."""
    # Get client IP and user agent
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    # Create submission record
    submission = ContactSubmission(
        name=contact_data.name,
        phone=contact_data.phone,
        email=contact_data.email,
        message=contact_data.message,
        ip_address=client_ip,
        user_agent=user_agent,
        status="new"
    )
    
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    # Send emails asynchronously
    try:
        await send_contact_notification(
            contact_data.name,
            contact_data.email,
            contact_data.phone,
            contact_data.message
        )
        await send_contact_confirmation(
            contact_data.email,
            contact_data.name
        )
    except Exception as e:
        print(f"Email sending failed: {e}")
        # Don't fail the request, submission was already saved
    
    return submission


@router.get("/admin/contact-submissions", response_model=List[ContactSubmissionDetail])
async def get_contact_submissions(
    status_filter: str = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Get all contact submissions (admin only)."""
    query = db.query(ContactSubmission)
    
    if status_filter:
        query = query.filter(ContactSubmission.status == status_filter)
    
    submissions = query.order_by(
        ContactSubmission.submitted_at.desc()
    ).offset(offset).limit(limit).all()
    
    return submissions


@router.get("/admin/contact-submissions/{submission_id}", response_model=ContactSubmissionDetail)
async def get_contact_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Get a specific contact submission (admin only)."""
    submission = db.query(ContactSubmission).filter(
        ContactSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact submission not found"
        )
    
    # Mark as read if status is new
    if submission.status == "new":
        submission.status = "read"
        db.commit()
    
    return submission


@router.patch("/admin/contact-submissions/{submission_id}/status")
async def update_submission_status(
    submission_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Update contact submission status (admin only)."""
    submission = db.query(ContactSubmission).filter(
        ContactSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact submission not found"
        )
    
    if status_value not in ["new", "read", "replied"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status. Must be: new, read, or replied"
        )
    
    submission.status = status_value
    db.commit()
    db.refresh(submission)
    
    return {"success": True, "submission": ContactSubmissionDetail.from_orm(submission)}


@router.delete("/admin/contact-submissions/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Delete a contact submission (admin only)."""
    submission = db.query(ContactSubmission).filter(
        ContactSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact submission not found"
        )
    
    db.delete(submission)
    db.commit()


# ============ Company Info Endpoints ============

@router.get("/company-info", response_model=CompanyInfoResponse)
async def get_company_info(
    db: Session = Depends(get_db)
):
    """Get company information."""
    # Try to get from cache
    cache_key = CACHE_KEYS['company_info']
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    company = db.query(CompanyInfo).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company info not configured"
        )
    
    # Cache result
    await set_cache(
        cache_key,
        CompanyInfoResponse.from_orm(company).dict(),
        ttl=CACHE_TTL['company_info']
    )
    
    return company


@router.put("/admin/company-info", response_model=CompanyInfoResponse)
async def update_company_info(
    company_data: CompanyInfoUpdate,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Update company information (admin only)."""
    company = db.query(CompanyInfo).first()
    
    if not company:
        # Create if doesn't exist
        company = CompanyInfo()
        db.add(company)
    
    update_data = company_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
    db.commit()
    db.refresh(company)
    
    # Invalidate cache
    await delete_cache(CACHE_KEYS['company_info'])
    
    return company


# ============ Statistics Endpoints ============

@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics(
    db: Session = Depends(get_db)
):
    """Get statistics."""
    # Try to get from cache
    cache_key = CACHE_KEYS['statistics']
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    stats = db.query(Statistics).first()
    if not stats:
        # Create default stats if don't exist
        stats = Statistics(
            annual_projects=1000,
            service_types=9,
            employees=90,
            satisfied_clients=100
        )
        db.add(stats)
        db.commit()
        db.refresh(stats)
    
    # Cache result
    await set_cache(
        cache_key,
        StatisticsResponse.from_orm(stats).dict(),
        ttl=CACHE_TTL['statistics']
    )
    
    return stats


@router.put("/admin/statistics", response_model=StatisticsResponse)
async def update_statistics(
    stats_data: StatisticsUpdate,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Update statistics (admin only)."""
    stats = db.query(Statistics).first()
    
    if not stats:
        stats = Statistics()
        db.add(stats)
    
    update_data = stats_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stats, field, value)
    
    db.commit()
    db.refresh(stats)
    
    # Invalidate cache
    await delete_cache(CACHE_KEYS['statistics'])
    
    return stats
