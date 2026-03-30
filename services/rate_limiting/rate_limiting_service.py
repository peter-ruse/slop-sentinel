import logging
import time

from services.redis_service import RedisService

logger = logging.getLogger(__name__)


class RateLimitingService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.__class__._initialized:
            return

        self.client = RedisService().client

        self.__class__._initialized = True

    async def is_rate_limited(self, key: str, limit: int, window: int) -> bool:
        key = f"rate-limit:{key}"
        pipeline = self.client.pipeline(transaction=True)
        now = time.time()
        window_start = now - window

        try:
            pipeline.zremrangebyscore(key, 0, window_start)
            pipeline.zadd(key, {str(now): now})
            pipeline.zcard(key)
            pipeline.expire(key, window + 1)

            _, _, current_count, _ = await pipeline.execute()

            return current_count > limit
        except Exception as e:
            logger.error(f"Rate limiter error: {e}")
            return False
