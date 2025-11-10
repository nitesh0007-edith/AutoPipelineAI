"""
Cache Manager - Unified interface for caching with multiple backends
"""
import hashlib
import pickle
from typing import Any, Optional, Callable
from functools import wraps
from loguru import logger
from pathlib import Path
import json
from datetime import datetime, timedelta


class CacheManager:
    """Manage caching with disk and memory backends"""

    def __init__(self, cache_dir: str = "data/cache", ttl_seconds: int = 3600):
        """
        Initialize cache manager

        Args:
            cache_dir: Directory for disk cache
            ttl_seconds: Time-to-live for cache entries in seconds
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.ttl_seconds = ttl_seconds
        self.memory_cache = {}
        self.cache_metadata = {}

        logger.info(f"Initialized CacheManager with dir: {cache_dir}, TTL: {ttl_seconds}s")

    def _generate_key(self, key_data: Any) -> str:
        """
        Generate cache key from data

        Args:
            key_data: Data to generate key from

        Returns:
            Hash string as cache key
        """
        if isinstance(key_data, str):
            key_str = key_data
        else:
            key_str = json.dumps(key_data, sort_keys=True, default=str)

        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, key: str, backend: str = "memory") -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key
            backend: 'memory' or 'disk'

        Returns:
            Cached value or None if not found/expired
        """
        cache_key = self._generate_key(key)

        # Check if expired
        if cache_key in self.cache_metadata:
            metadata = self.cache_metadata[cache_key]
            expires_at = metadata.get("expires_at")

            if expires_at and datetime.now() > expires_at:
                logger.debug(f"Cache expired for key: {key[:50]}")
                self.delete(key, backend)
                return None

        if backend == "memory":
            value = self.memory_cache.get(cache_key)
            if value is not None:
                logger.debug(f"Cache HIT (memory): {key[:50]}")
            return value

        elif backend == "disk":
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            if cache_file.exists():
                try:
                    with open(cache_file, "rb") as f:
                        value = pickle.load(f)
                    logger.debug(f"Cache HIT (disk): {key[:50]}")
                    return value
                except Exception as e:
                    logger.warning(f"Failed to load cache: {e}")
                    return None

        logger.debug(f"Cache MISS: {key[:50]}")
        return None

    def set(self, key: str, value: Any, backend: str = "memory", ttl_seconds: Optional[int] = None) -> bool:
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            backend: 'memory' or 'disk'
            ttl_seconds: Custom TTL, or use default

        Returns:
            True if successful
        """
        cache_key = self._generate_key(key)
        ttl = ttl_seconds or self.ttl_seconds

        # Set expiration metadata
        self.cache_metadata[cache_key] = {
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(seconds=ttl),
            "original_key": key[:100]  # Store truncated key for debugging
        }

        try:
            if backend == "memory":
                self.memory_cache[cache_key] = value
                logger.debug(f"Cached to memory: {key[:50]}")

            elif backend == "disk":
                cache_file = self.cache_dir / f"{cache_key}.pkl"
                with open(cache_file, "wb") as f:
                    pickle.dump(value, f)
                logger.debug(f"Cached to disk: {key[:50]}")

            return True

        except Exception as e:
            logger.error(f"Failed to cache: {e}")
            return False

    def delete(self, key: str, backend: str = "memory") -> bool:
        """
        Delete value from cache

        Args:
            key: Cache key
            backend: 'memory' or 'disk'

        Returns:
            True if successful
        """
        cache_key = self._generate_key(key)

        try:
            if backend == "memory":
                if cache_key in self.memory_cache:
                    del self.memory_cache[cache_key]

            elif backend == "disk":
                cache_file = self.cache_dir / f"{cache_key}.pkl"
                if cache_file.exists():
                    cache_file.unlink()

            if cache_key in self.cache_metadata:
                del self.cache_metadata[cache_key]

            logger.debug(f"Deleted cache: {key[:50]}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete cache: {e}")
            return False

    def clear(self, backend: str = "both") -> bool:
        """
        Clear all cache

        Args:
            backend: 'memory', 'disk', or 'both'

        Returns:
            True if successful
        """
        try:
            if backend in ["memory", "both"]:
                self.memory_cache.clear()
                logger.info("Cleared memory cache")

            if backend in ["disk", "both"]:
                for cache_file in self.cache_dir.glob("*.pkl"):
                    cache_file.unlink()
                logger.info("Cleared disk cache")

            self.cache_metadata.clear()
            return True

        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
            return False

    def get_stats(self) -> dict:
        """
        Get cache statistics

        Returns:
            Dictionary with cache stats
        """
        disk_files = list(self.cache_dir.glob("*.pkl"))
        disk_size = sum(f.stat().st_size for f in disk_files)

        return {
            "memory_entries": len(self.memory_cache),
            "disk_entries": len(disk_files),
            "disk_size_mb": disk_size / (1024 * 1024),
            "ttl_seconds": self.ttl_seconds,
            "metadata_entries": len(self.cache_metadata)
        }

    def cached(self, backend: str = "memory", ttl_seconds: Optional[int] = None):
        """
        Decorator for caching function results

        Args:
            backend: Cache backend to use
            ttl_seconds: Custom TTL

        Returns:
            Decorated function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key from function name and arguments
                cache_key = f"{func.__name__}:{args}:{kwargs}"

                # Try to get from cache
                cached_value = self.get(cache_key, backend)
                if cached_value is not None:
                    return cached_value

                # Execute function
                result = func(*args, **kwargs)

                # Cache result
                self.set(cache_key, result, backend, ttl_seconds)

                return result

            return wrapper
        return decorator
