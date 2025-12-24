import redis
import json
from typing import Optional, Any
from app.core.config import get_settings

settings = get_settings()

# Redis client
redis_client: Optional[redis.Redis] = None


def init_redis():
    """Initialize Redis connection."""
    global redis_client
    try:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        redis_client.ping()
        print("✓ Redis connected successfully")
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")
        redis_client = None


async def get_cached(key: str) -> Optional[Any]:
    """Get cached value."""
    if redis_client is None:
        return None
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        print(f"Cache get error: {e}")
    return None


async def set_cache(key: str, value: Any, ttl: int = 3600):
    """Set cached value with TTL."""
    if redis_client is None:
        return
    try:
        redis_client.setex(key, ttl, json.dumps(value, default=str))
    except Exception as e:
        print(f"Cache set error: {e}")


async def delete_cache(key: str):
    """Delete cached value."""
    if redis_client is None:
        return
    try:
        redis_client.delete(key)
    except Exception as e:
        print(f"Cache delete error: {e}")


async def invalidate_pattern(pattern: str):
    """Invalidate cache keys matching pattern."""
    if redis_client is None:
        return
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception as e:
        print(f"Cache invalidate error: {e}")


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
}


# TTL values (in seconds)
CACHE_TTL = {
    "services": 3600,  # 1 hour
    "team": 3600,
    "certificates": 3600,
    "licenses": 3600,
    "company_info": 7200,  # 2 hours
    "statistics": 7200,
}
