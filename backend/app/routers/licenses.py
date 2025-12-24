from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime

from app.database import get_db
from app.models.models import License
from app.schemas.schemas import (
    LicenseCreate, LicenseUpdate, LicenseResponse
)
from app.core.security import require_admin
from app.cache import (
    get_cached, set_cache, delete_cache,
    CACHE_KEYS, CACHE_TTL
)

router = APIRouter(prefix="/licenses", tags=["Licenses"])

UPLOAD_DIR = "/home/unique/projects/geobiro/backend/uploads/licenses"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("", response_model=List[LicenseResponse])
async def get_licenses(
    db: Session = Depends(get_db)
):
    """Get all licenses."""
    # Try to get from cache
    cache_key = CACHE_KEYS['licenses']
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    licenses = db.query(License).order_by(License.created_at.desc()).all()
    
    # Cache result
    await set_cache(
        cache_key,
        [LicenseResponse.from_orm(l).dict() for l in licenses],
        ttl=CACHE_TTL['licenses']
    )
    
    return licenses


@router.get("/{license_id}", response_model=LicenseResponse)
async def get_license(
    license_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific license."""
    license = db.query(License).filter(License.id == license_id).first()
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    return license


@router.post("", response_model=LicenseResponse, status_code=status.HTTP_201_CREATED)
async def create_license(
    license_data: LicenseCreate,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Create a new license (admin only)."""
    new_license = License(**license_data.dict())
    db.add(new_license)
    db.commit()
    db.refresh(new_license)
    
    # Invalidate cache
    await delete_cache(CACHE_KEYS['licenses'])
    
    return new_license


@router.post("/{license_id}/upload-image")
async def upload_license_image(
    license_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Upload image for license."""
    license = db.query(License).filter(License.id == license_id).first()
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
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
    filename = f"license_{license_id}_{timestamp}{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update license with image URL
    image_url = f"/uploads/licenses/{filename}"
    license.image_url = image_url
    db.commit()
    db.refresh(license)
    
    # Invalidate cache
    await delete_cache(CACHE_KEYS['licenses'])
    
    return {
        "success": True,
        "image_url": image_url,
        "license": LicenseResponse.from_orm(license)
    }


@router.put("/{license_id}", response_model=LicenseResponse)
async def update_license(
    license_id: int,
    license_data: LicenseUpdate,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Update a license (admin only)."""
    license = db.query(License).filter(License.id == license_id).first()
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    update_data = license_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(license, field, value)
    
    db.commit()
    db.refresh(license)
    
    # Invalidate cache
    await delete_cache(CACHE_KEYS['licenses'])
    
    return license


@router.delete("/{license_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_license(
    license_id: int,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Delete a license (admin only)."""
    license = db.query(License).filter(License.id == license_id).first()
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    db.delete(license)
    db.commit()
    
    # Invalidate cache
    await delete_cache(CACHE_KEYS['licenses'])
