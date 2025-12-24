from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Service
from app.schemas.schemas import ServiceCreate, ServiceUpdate, ServiceResponse
from app.core.security import require_admin
from app.cache import (
    get_cached, set_cache, delete_cache, invalidate_pattern,
    CACHE_KEYS, CACHE_TTL
)

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("", response_model=List[ServiceResponse])
async def get_services(
    category: str = Query(None, description="Filter by category: BIM or Surveying"),
    db: Session = Depends(get_db)
):
    """Get all services with optional category filter."""
    # Try to get from cache
    cache_key = f"{CACHE_KEYS['services']}:{category}" if category else CACHE_KEYS['services']
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    # Query database
    query = db.query(Service)
    if category:
        query = query.filter(Service.category == category)
    
    services = query.order_by(Service.created_at.desc()).all()
    
    # Cache result
    await set_cache(
        cache_key,
        [ServiceResponse.from_orm(s).dict() for s in services],
        ttl=CACHE_TTL['services']
    )
    
    return services


@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific service by ID."""
    # Try to get from cache
    cache_key = CACHE_KEYS['service_detail'].format(id=service_id)
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Cache result
    await set_cache(
        cache_key,
        ServiceResponse.from_orm(service).dict(),
        ttl=CACHE_TTL['services']
    )
    
    return service


@router.post("", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Create a new service (admin only)."""
    # Validate category
    if service_data.category not in ["BIM", "Surveying"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category must be 'BIM' or 'Surveying'"
        )
    
    new_service = Service(**service_data.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['services'] + "*")
    
    return new_service


@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Update a service (admin only)."""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    update_data = service_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)
    
    db.commit()
    db.refresh(service)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['services'] + "*")
    cache_key = CACHE_KEYS['service_detail'].format(id=service_id)
    await delete_cache(cache_key)
    
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    admin: object = Depends(require_admin)
):
    """Delete a service (admin only)."""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    db.delete(service)
    db.commit()
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['services'] + "*")
    cache_key = CACHE_KEYS['service_detail'].format(id=service_id)
    await delete_cache(cache_key)
