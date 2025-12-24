from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Article
from app.schemas.schemas import ArticleCreate, ArticleUpdate, ArticleResponse
from app.core.security import require_admin
from app.cache import (
    get_cached, set_cache, delete_cache, invalidate_pattern,
    CACHE_KEYS, CACHE_TTL
)

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("", response_model=List[ArticleResponse])
async def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    tag: str = Query(None, description="Filter by tag"),
    category: str = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """Get articles with pagination and optional filtering."""
    # Build cache key
    cache_key_parts = [CACHE_KEYS['articles']]
    if tag:
        cache_key_parts.append(f"tag:{tag}")
    if category:
        cache_key_parts.append(f"category:{category}")
    cache_key_parts.extend([f"skip:{skip}", f"limit:{limit}"])
    
    cache_key = ":".join(cache_key_parts)
    
    # Try cache
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    # Query database
    query = db.query(Article).filter(Article.is_published == True).order_by(Article.publish_date.desc())
    
    if tag:
        query = query.filter(Article.tags.contains(tag))
    if category:
        query = query.filter(Article.category == category)
    
    articles = query.offset(skip).limit(limit).all()
    
    # Cache result
    await set_cache(
        cache_key,
        [ArticleResponse.from_orm(a).dict() for a in articles],
        ttl=CACHE_TTL['articles']
    )
    
    return articles


@router.get("/{article_id_or_slug}", response_model=ArticleResponse)
async def get_article(
    article_id_or_slug: str,
    db: Session = Depends(get_db)
):
    """Get a specific article by ID or slug."""
    # Try cache
    cache_key = f"{CACHE_KEYS['articles']}:{article_id_or_slug}"
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data
    
    # Try to get by ID first (if numeric)
    article = None
    if article_id_or_slug.isdigit():
        article = db.query(Article).filter(Article.id == int(article_id_or_slug)).first()
    
    # If not found by ID, try by slug
    if not article:
        article = db.query(Article).filter(Article.slug == article_id_or_slug).first()
    
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    # Cache result
    await set_cache(
        cache_key,
        ArticleResponse.from_orm(article).dict(),
        ttl=CACHE_TTL['articles']
    )
    
    return article


@router.post("", response_model=ArticleResponse, dependencies=[Depends(require_admin)])
async def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db)
):
    """Create a new article (admin only)."""
    # Check for duplicate slug
    existing = db.query(Article).filter(Article.slug == article.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article with this slug already exists"
        )
    
    db_article = Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['articles'])
    
    return db_article


@router.put("/{article_id}", response_model=ArticleResponse, dependencies=[Depends(require_admin)])
async def update_article(
    article_id: int,
    article: ArticleUpdate,
    db: Session = Depends(get_db)
):
    """Update an article (admin only)."""
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    update_data = article.dict(exclude_unset=True)
    
    # Check for duplicate slug if slug is being updated
    if 'slug' in update_data and update_data['slug'] != db_article.slug:
        existing = db.query(Article).filter(
            Article.slug == update_data['slug'],
            Article.id != article_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Article with this slug already exists"
            )
    
    for field, value in update_data.items():
        setattr(db_article, field, value)
    
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['articles'])
    
    return db_article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
async def delete_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """Delete an article (admin only)."""
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    db.delete(db_article)
    db.commit()
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['articles'])
    
    return None


@router.get("/tags/all", response_model=List[str])
async def get_all_tags(db: Session = Depends(get_db)):
    """Get all unique tags from published articles."""
    articles = db.query(Article).filter(Article.is_published == True).all()
    tags_set = set()
    
    for article in articles:
        if article.tags:
            tags = [tag.strip() for tag in article.tags.split(',')]
            tags_set.update(tags)
    
    return sorted(list(tags_set))
