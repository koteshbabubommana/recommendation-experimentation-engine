import json
import os

try:
    import redis
except ImportError:
    redis = None


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class RedisCache:
    def __init__(self):
        self.client = None

        if redis:
            try:
                self.client = redis.from_url(REDIS_URL, decode_responses=True)
                self.client.ping()
            except Exception:
                self.client = None

    def get(self, key: str):
        if not self.client:
            return None

        value = self.client.get(key)

        if value:
            return json.loads(value)

        return None

    def set(self, key: str, value: dict, ttl: int = 300):
        if not self.client:
            return False

        self.client.setex(key, ttl, json.dumps(value))
        return True


cache = RedisCache()