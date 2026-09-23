import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 24 hours in seconds: 24 * 60 * 60 = 86,400
CACHE_TTL_SECONDS = 86400

# decode_responses=True ensures Redis returns standard Python strings instead of raw bytes
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def get_cached_url(short_code: str) -> str | None:
    """Attempts to fetch the long URL from Redis. Returns None if not found or if Redis is offline."""
    try:
        return redis_client.get(short_code)
    except Exception as e:
        print(f"[CACHE WARNING] Redis lookup failed: {e}. Falling back to PostgreSQL.")
        return None


def set_cached_url(short_code: str, long_url: str) -> None:
    """Saves the short_code -> long_url pair into Redis with a 24-hour TTL."""
    try:
        redis_client.set(short_code, long_url, ex=CACHE_TTL_SECONDS)
    except Exception as e:
        print(f"[CACHE WARNING] Redis write failed: {e}.")