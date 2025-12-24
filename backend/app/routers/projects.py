from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Project
from app.schemas.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.core.security import require_admin
from app.cache import (
    get_cached, set_cache, delete_cache, invalidate_pattern,
    CACHE_KEYS, CACHE_TTL
)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    category: str = Query(None, description="Filter by category"),
    featured: bool = Query(None, description="Filter by featured status"),
    db: Session = Depends(get_db)
):
    """Get all projects with optional filtering."""
    # Build cache key
    cache_key_parts = [CACHE_KEYS['projects']]
    if category:
        cache_key_parts.append(f"category:{category}")
    if featured is not None:
        cache_key_parts.append(f"featured:{featured}")
    
    cache_key = ":".join(cache_key_parts) if len(cache_key_parts) > 1 else CACHE_KEYS['projects']
    
    # Try to get from cache
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    # Query database
    query = db.query(Project).order_by(Project.order, Project.created_at.desc())
    
    if category:
        query = query.filter(Project.category == category)
    if featured is not None:
        query = query.filter(Project.is_featured == featured)
    
    projects = query.all()
    
    # Cache result
    await set_cache(
        cache_key,
        [ProjectResponse.from_orm(p).dict() for p in projects],
        ttl=CACHE_TTL['projects']
    )
    
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific project by ID."""
    # Try cache
    cache_key = f"{CACHE_KEYS['projects']}:{project_id}"
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    # Cache result
    await set_cache(
        cache_key,
        ProjectResponse.from_orm(project).dict(),
        ttl=CACHE_TTL['projects']
    )
    
    return project


@router.post("", response_model=ProjectResponse, dependencies=[Depends(require_admin)])
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project (admin only)."""
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['projects'])
    
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse, dependencies=[Depends(require_admin)])
async def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Update a project (admin only)."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    update_data = project.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['projects'])
    
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Delete a project (admin only)."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['projects'])
    
    return None
