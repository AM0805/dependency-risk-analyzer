import time

TTL = 86400        # 24 hours in seconds
MAX_CACHE_SIZE = 500

# { "package_name": { "data": {...}, "timestamp": float } }
_cache: dict = {}


def _normalize(key: str) -> str:
    return key.strip().lower()


def is_cache_valid(timestamp: float) -> bool:
    return (time.time() - timestamp) < TTL


def get_from_cache(key: str) -> dict | None:
    key = _normalize(key)
    entry = _cache.get(key)

    if entry is None:
        return None

    if not is_cache_valid(entry["timestamp"]):
        print(f"CACHE EXPIRED: {key}")
        del _cache[key]
        return None

    print(f"CACHE HIT: {key}")
    return entry["data"]


def set_cache(key: str, data: dict) -> None:
    key = _normalize(key)

    # Evict oldest entry if at capacity
    if len(_cache) >= MAX_CACHE_SIZE and key not in _cache:
        oldest_key = min(_cache, key=lambda k: _cache[k]["timestamp"])
        del _cache[oldest_key]

    _cache[key] = {
        "data": data,
        "timestamp": time.time(),
    }
