from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Article, ArticleImage
from app.schemas.schemas import (
    ArticleCreate, ArticleUpdate, ArticleResponse,
    ArticleImageCreate, ArticleImageUpdate, ArticleImageResponse
)
from app.core.security import require_admin
from app.cache import (
    get_cached, set_cache, delete_cache, invalidate_pattern,
    CACHE_KEYS, CACHE_TTL
)

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("", response_model=List[ArticleResponse])
async def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    tag: str = Query(None, description="Filter by tag"),
    category: str = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """Get articles with pagination and optional filtering."""
    # Query database
    query = db.query(Article).filter(Article.is_published == True).order_by(Article.publish_date.desc())
    
    if tag:
        query = query.filter(Article.tags.contains(tag))
    if category:
        query = query.filter(Article.category == category)
    
    articles = query.offset(skip).limit(limit).all()
    
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


@router.post("/seed-demo", response_model=dict)
async def seed_demo_articles(db: Session = Depends(get_db)):
    """Seed demo articles for development. (Development only)"""
    from datetime import datetime, timedelta
    
    # Check if articles already exist
    existing = db.query(Article).count()
    if existing > 0:
        return {"message": f"Articles already exist: {existing} articles found"}
    
    sample_articles = [
        Article(
            title_en="Introduction to BIM Technology",
            title_fa="معرفی فناوری BIM",
            slug="introduction-to-bim",
            summary_en="Learn the basics of Building Information Modeling and its impact on modern construction.",
            summary_fa="آشنایی با اصول مدل‌سازی اطلاعات ساختمان و تاثیر آن بر ساخت و ساز مدرن",
            content_en="<p>BIM (Building Information Modeling) is a comprehensive approach to building design, construction, and management.</p>",
            content_fa="<p>BIM (مدل‌سازی اطلاعات ساختمان) روشی جامع برای طراحی، ساخت و مدیریت ساختمان است.</p>",
            category="BIM",
            author="Geobiro Team",
            tags="BIM, technology, construction",
            is_published=True,
            publish_date=datetime.utcnow() - timedelta(days=7)
        ),
        Article(
            title_en="Surveying: The Foundation of Construction",
            title_fa="نقشه‌برداری: بنیان ساخت و ساز",
            slug="surveying-foundation-construction",
            summary_en="Explore the essential role of surveying in modern construction projects.",
            summary_fa="بررسی نقش حیاتی نقشه‌برداری در پروژه‌های ساخت و ساز مدرن",
            content_en="<p>Surveying is the process of determining positions and distances in the landscape.</p>",
            content_fa="<p>نقشه‌برداری فرایند تعیین موقعیت‌ها و فاصله‌ها در سرزمین است.</p>",
            category="Surveying",
            author="Geobiro Team",
            tags="surveying, GPS, mapping",
            is_published=True,
            publish_date=datetime.utcnow() - timedelta(days=5)
        ),
        Article(
            title_en="Latest Updates in Geospatial Technology",
            title_fa="آخرین به‌روزرسانی‌های فناوری جغرافیایی",
            slug="geospatial-technology-updates",
            summary_en="Stay informed about the latest developments in geospatial technology.",
            summary_fa="از آخرین پیشرفت‌های فناوری جغرافیایی آگاه بمانید",
            content_en="<p>Geospatial technology is rapidly evolving with new tools and methodologies.</p>",
            content_fa="<p>فناوری جغرافیایی به سرعت در حال تکامل است.</p>",
            category="Technology",
            author="Geobiro Team",
            tags="geospatial, AI, technology",
            is_published=True,
            publish_date=datetime.utcnow() - timedelta(days=3)
        ),
        Article(
            title_en="Success Stories: BIM in Large-Scale Projects",
            title_fa="داستان‌های موفقیت: BIM در پروژه‌های بزرگ",
            slug="bim-success-stories",
            summary_en="Learn how BIM has revolutionized major construction projects.",
            summary_fa="بیاموزید چگونه BIM پروژه‌های ساخت و ساز بزرگ را متحول کرده است",
            content_en="<p>Major infrastructure projects have successfully implemented BIM.</p>",
            content_fa="<p>پروژه‌های زیربنایی بزرگ با موفقیت BIM را پیاده‌سازی کرده‌اند.</p>",
            category="BIM",
            author="Geobiro Team",
            tags="BIM, projects, infrastructure",
            is_published=True,
            publish_date=datetime.utcnow() - timedelta(days=1)
        ),
        Article(
            title_en="Drone Technology in Land Surveying",
            title_fa="فناوری درون‌بین در نقشه‌برداری زمین",
            slug="drone-surveying-technology",
            summary_en="Discover how drones are transforming surveying and mapping practices.",
            summary_fa="کشف کنید چگونه درون‌بین‌ها عملیات نقشه‌برداری را تغییر می‌دهند",
            content_en="<p>Unmanned Aerial Vehicles have become indispensable tools in surveying.</p>",
            content_fa="<p>خودروهای بدون سرنشین به ابزارهای ضروری در نقشه‌برداری تبدیل شده‌اند.</p>",
            category="Surveying",
            author="Geobiro Team",
            tags="drone, surveying, UAV",
            is_published=True,
            publish_date=datetime.utcnow()
        )
    ]
    
    db.add_all(sample_articles)
    db.commit()
    
    return {
        "message": f"Successfully seeded {len(sample_articles)} demo articles",
        "count": len(sample_articles)
    }


# ============ Article Images Endpoints ============

@router.post("/{article_id}/images", response_model=ArticleImageResponse, dependencies=[Depends(require_admin)])
async def add_article_image(
    article_id: int,
    image: ArticleImageCreate,
    db: Session = Depends(get_db)
):
    """Add an image to an article (admin only)."""
    # Check if article exists
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    # Create image record
    db_image = ArticleImage(article_id=article_id, **image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['articles'])
    
    return db_image


@router.get("/{article_id}/images", response_model=List[ArticleImageResponse])
async def get_article_images(
    article_id: int,
    db: Session = Depends(get_db)
):
    """Get all images for an article."""
    # Check if article exists
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    images = db.query(ArticleImage).filter(
        ArticleImage.article_id == article_id
    ).order_by(ArticleImage.order).all()
    
    return images


@router.put("/{article_id}/images/{image_id}", response_model=ArticleImageResponse, dependencies=[Depends(require_admin)])
async def update_article_image(
    article_id: int,
    image_id: int,
    image: ArticleImageUpdate,
    db: Session = Depends(get_db)
):
    """Update an article image (admin only)."""
    # Check if image exists and belongs to article
    db_image = db.query(ArticleImage).filter(
        ArticleImage.id == image_id,
        ArticleImage.article_id == article_id
    ).first()
    
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found or does not belong to this article"
        )
    
    # Update image fields
    update_data = image.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_image, field, value)
    
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['articles'])
    
    return db_image


@router.delete("/{article_id}/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
async def delete_article_image(
    article_id: int,
    image_id: int,
    db: Session = Depends(get_db)
):
    """Delete an article image (admin only)."""
    # Check if image exists and belongs to article
    db_image = db.query(ArticleImage).filter(
        ArticleImage.id == image_id,
        ArticleImage.article_id == article_id
    ).first()
    
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found or does not belong to this article"
        )
    
    db.delete(db_image)
    db.commit()
    
    # Invalidate cache
    await invalidate_pattern(CACHE_KEYS['articles'])
    
    return None
