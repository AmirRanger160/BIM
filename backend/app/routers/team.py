from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import datetime

from app.database import get_db
from app.models.models import TeamMember
from app.schemas.schemas import (
    TeamMemberCreate, TeamMemberUpdate, TeamMemberResponse
)
from app.core.security import require_admin
from app.cache import (
    get_cached, set_cache, delete_cache, invalidate_pattern,
    CACHE_KEYS, CACHE_TTL
)

router = APIRouter(prefix="/team", tags=["Team"])

UPLOAD_DIR = "/home/unique/projects/geobiro/backend/uploads/team"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("", response_model=List[TeamMemberResponse])
async def get_team_members(
    db: Session = Depends(get_db)
):
    """Get all team members."""
    # Try to get from cache
    cache_key = CACHE_KEYS['team']
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    members = db.query(TeamMember).order_by(TeamMember.created_at.desc()).all()
    
    # Cache result
    await set_cache(
        cache_key,
        [TeamMemberResponse.from_orm(m).dict() for m in members],
        ttl=CACHE_TTL['team']
    )
    
    return members


@router.get("/{member_id}", response_model=TeamMemberResponse)
async def get_team_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific team member."""
    # Try to get from cache
    cache_key = CACHE_KEYS['team_member'].format(id=member_id)
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found"
        )
    
    # Cache result
    await set_cache(
        cache_key,
        TeamMemberResponse.from_orm(member).dict(),
        ttl=CACHE_TTL['team']
    )
    
    return member


@router.post("", response_model=TeamMemberResponse, status_code=status.HTTP_201_CREATED)
async def create_team_member(
    member_data: TeamMemberCreate,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Create a new team member (admin only)."""
    new_member = TeamMember(**member_data.dict())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['team'] + "*")
    
    return new_member


@router.post("/{member_id}/upload-image")
async def upload_team_member_image(
    member_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Upload image for team member."""
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found"
        )
    
    # Validate file type
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Allowed: jpg, jpeg, png, webp, gif"
        )
    
    # Save file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"member_{member_id}_{timestamp}{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update member with image URL
    image_url = f"/uploads/team/{filename}"
    member.image_url = image_url
    db.commit()
    db.refresh(member)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['team'] + "*")
    cache_key = CACHE_KEYS['team_member'].format(id=member_id)
    await delete_cache(cache_key)
    
    return {
        "success": True,
        "image_url": image_url,
        "member": TeamMemberResponse.from_orm(member)
    }


@router.put("/{member_id}", response_model=TeamMemberResponse)
async def update_team_member(
    member_id: int,
    member_data: TeamMemberUpdate,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Update a team member (admin only)."""
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found"
        )
    
    update_data = member_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(member, field, value)
    
    db.commit()
    db.refresh(member)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['team'] + "*")
    cache_key = CACHE_KEYS['team_member'].format(id=member_id)
    await delete_cache(cache_key)
    
    return member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team_member(
    member_id: int,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Delete a team member (admin only)."""
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found"
        )
    
    db.delete(member)
    db.commit()
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['team'] + "*")
    cache_key = CACHE_KEYS['team_member'].format(id=member_id)
    await delete_cache(cache_key)
