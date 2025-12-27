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
    
    # Convert services to response format with proper field mapping
    response_list = []
    for s in services:
        service_dict = {
            'id': s.id,
            'title': s.title,
            'title_en': s.title_en or s.title,
            'title_fa': s.title_fa,
            'description': s.description,
            'description_en': s.description_en or s.description,
            'description_fa': s.description_fa,
            'category': s.category,
            'image_url': s.image_url,
            'software_tools': s.software_tools,
            'created_at': s.created_at,
            'updated_at': s.updated_at,
        }
        response_list.append(service_dict)
    
    # Cache result
    await set_cache(
        cache_key,
        response_list,
        ttl=CACHE_TTL['services']
    )
    
    return response_list


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
    
    # Convert to response format with proper field mapping
    service_dict = {
        'id': service.id,
        'title': service.title,
        'title_en': service.title_en or service.title,
        'title_fa': service.title_fa,
        'description': service.description,
        'description_en': service.description_en or service.description,
        'description_fa': service.description_fa,
        'category': service.category,
        'image_url': service.image_url,
        'software_tools': service.software_tools,
        'created_at': service.created_at,
        'updated_at': service.updated_at,
    }
    
    # Cache result
    await set_cache(
        cache_key,
        service_dict,
        ttl=CACHE_TTL['services']
    )
    
    return service_dict


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
    
    # Convert to dict and handle field mapping
    data = service_data.dict(exclude_none=True)
    
    # Handle bilingual fields: ensure both old and new formats are stored
    if data.get('title_en'):
        data['title'] = data['title_en']
    if data.get('title') and not data.get('title_en'):
        data['title_en'] = data['title']
    
    if data.get('description_en'):
        data['description'] = data['description_en']
    if data.get('description') and not data.get('description_en'):
        data['description_en'] = data['description']
    
    new_service = Service(**data)
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
