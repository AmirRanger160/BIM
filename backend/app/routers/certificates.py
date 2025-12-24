from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime

from app.database import get_db
from app.models.models import Certificate
from app.schemas.schemas import (
    CertificateCreate, CertificateUpdate, CertificateResponse
)
from app.core.security import require_admin
from app.cache import (
    get_cached, set_cache, delete_cache, invalidate_pattern,
    CACHE_KEYS, CACHE_TTL
)

router = APIRouter(prefix="/certificates", tags=["Certificates"])

UPLOAD_DIR = "/home/unique/projects/geobiro/backend/uploads/certificates"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("", response_model=List[CertificateResponse])
async def get_certificates(
    db: Session = Depends(get_db)
):
    """Get all certificates."""
    # Try to get from cache
    cache_key = CACHE_KEYS['certificates']
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    certificates = db.query(Certificate).order_by(Certificate.created_at.desc()).all()
    
    # Cache result
    await set_cache(
        cache_key,
        [CertificateResponse.from_orm(c).dict() for c in certificates],
        ttl=CACHE_TTL['certificates']
    )
    
    return certificates


@router.get("/{cert_id}", response_model=CertificateResponse)
async def get_certificate(
    cert_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific certificate."""
    certificate = db.query(Certificate).filter(Certificate.id == cert_id).first()
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    return certificate


@router.post("", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
async def create_certificate(
    cert_data: CertificateCreate,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Create a new certificate (admin only)."""
    new_cert = Certificate(**cert_data.dict())
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    
    # Invalidate cache
    await delete_cache(CACHE_KEYS['certificates'])
    
    return new_cert


@router.post("/{cert_id}/upload-image")
async def upload_certificate_image(
    cert_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Upload image for certificate."""
    certificate = db.query(Certificate).filter(Certificate.id == cert_id).first()
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    
    # Validate file type
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type"
        )
    
    # Save file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cert_{cert_id}_{timestamp}{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update certificate with image URL
    image_url = f"/uploads/certificates/{filename}"
    certificate.image_url = image_url
    db.commit()
    db.refresh(certificate)
    
    # Invalidate cache
    await delete_cache(CACHE_KEYS['certificates'])
    
    return {
        "success": True,
        "image_url": image_url,
        "certificate": CertificateResponse.from_orm(certificate)
    }


@router.put("/{cert_id}", response_model=CertificateResponse)
async def update_certificate(
    cert_id: int,
    cert_data: CertificateUpdate,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Update a certificate (admin only)."""
    certificate = db.query(Certificate).filter(Certificate.id == cert_id).first()
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    
    update_data = cert_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(certificate, field, value)
    
    db.commit()
    db.refresh(certificate)
    
    # Invalidate cache
    await delete_cache(CACHE_KEYS['certificates'])
    
    return certificate


@router.delete("/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certificate(
    cert_id: int,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Delete a certificate (admin only)."""
    certificate = db.query(Certificate).filter(Certificate.id == cert_id).first()
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    
    db.delete(certificate)
    db.commit()
    
    # Invalidate cache
    await delete_cache(CACHE_KEYS['certificates'])
