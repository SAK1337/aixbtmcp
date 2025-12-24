"""Simple TTL-based cache for API responses."""

from datetime import datetime, timedelta
from typing import Any, Optional


class TTLCache:
    """In-memory cache with configurable TTL."""

    def __init__(self, default_ttl_seconds: int = 300) -> None:
        self._cache: dict[str, tuple[Any, datetime]] = {}
        self._default_ttl = timedelta(seconds=default_ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key not in self._cache:
            return None

        value, timestamp = self._cache[key]
        if datetime.now() - timestamp > self._default_ttl:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set cached value with optional custom TTL."""
        self._cache[key] = (value, datetime.now())

    def delete(self, key: str) -> bool:
        """Delete cached value. Returns True if key existed."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()

    def cleanup_expired(self) -> int:
        """Remove all expired entries. Returns count of removed entries."""
        now = datetime.now()
        expired_keys = [
            key
            for key, (_, timestamp) in self._cache.items()
            if now - timestamp > self._default_ttl
        ]
        for key in expired_keys:
            del self._cache[key]
        return len(expired_keys)


def make_cache_key(*args: Any, **kwargs: Any) -> str:
    """Generate a cache key from function arguments."""
    parts = [str(arg) for arg in args]
    parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None)
    return ":".join(parts)


# Global cache instance
_cache: Optional[TTLCache] = None


def get_cache(ttl_seconds: int = 300) -> TTLCache:
    """Get or create the global cache instance."""
    global _cache
    if _cache is None:
        _cache = TTLCache(default_ttl_seconds=ttl_seconds)
    return _cache


def get_cached(key: str) -> Optional[Any]:
    """Get value from global cache."""
    return get_cache().get(key)


def set_cache(key: str, value: Any) -> None:
    """Set value in global cache."""
    get_cache().set(key, value)
