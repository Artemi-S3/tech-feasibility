import os
import json
import redis
import time
import hashlib
from typing import Any

r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
NAMESPACE = "artemis3"
TTL = 300

def cache_key(*parts: str) -> str:
    h = hashlib.sha256("::".join(parts).encode()).hexdigest()
    return f"{NAMESPACE}:{h}"

def get_cached(bucket: str, key: str) -> Any | None:
    k = cache_key("s3meta", bucket, key)
    raw = r.get(k)
    return json.loads(raw) if raw else None

def set_cached(bucket: str, key: str, value: dict, ttl: int = TTL) -> None:
    k = cache_key("s3meta", bucket, key)
    r.setex(k, ttl, json.dumps(value))

def fetch_s3_head(bucket: str, key: str) -> dict:
    # simulate fetching
    time.sleep(0.3)
    return {"bucket": bucket, "key": key, "etag": "abcd", "size": 1234}

def get_meta(bucket: str, key: str) -> dict:
    cached = get_cached(bucket, key)
    if cached: return {"cached": True, "data": cached}

    data = fetch_s3_head(bucket, key)
    set_cached(bucket, key, data)
    return {"cached": False, "data": data}
