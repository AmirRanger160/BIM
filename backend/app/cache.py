"""
Cache module - Removed Redis dependency.
Cache functions are now stubs that do nothing.
"""
from typing import Optional, Any


def init_redis():
    """Initialize Redis connection - removed, does nothing."""
    print("✓ Cache initialization skipped (Redis removed)")


async def get_cached(key: str) -> Optional[Any]:
    """Get cached value - removed, always returns None."""
    return None


async def set_cache(key: str, value: Any, ttl: int = 3600):
    """Set cached value with TTL - removed, does nothing."""
    pass


async def delete_cache(key: str):
    """Delete cached value - removed, does nothing."""
    pass


async def invalidate_pattern(pattern: str):
    """Invalidate cache keys matching pattern - removed, does nothing."""
    pass


# Cache key prefixes
CACHE_KEYS = {
    "services": "cache:services",
    "service_detail": "cache:service:{id}",
    "team": "cache:team",
    "team_member": "cache:team:{id}",
    "certificates": "cache:certificates",
    "licenses": "cache:licenses",
    "company_info": "cache:company_info",
    "statistics": "cache:statistics",
    "projects": "cache:projects",
    "articles": "cache:articles",
}


# TTL values (in seconds)
CACHE_TTL = {
    "services": 3600,  # 1 hour
    "team": 3600,
    "certificates": 3600,
    "licenses": 3600,
    "company_info": 7200,  # 2 hours
    "statistics": 7200,
    "projects": 3600,
    "articles": 1800,  # 30 minutes for articles (more frequent updates)
}
