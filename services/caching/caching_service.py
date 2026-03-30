from core.config import RedisCacheSettings
from services.redis_service import RedisService


class CachingService:
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
        self.cache_ttl = RedisCacheSettings().cache_ttl

        self.__class__._initialized = True

    async def get(self, key: str):
        key = f"cache:{key}"
        return await self.client.get(key)

    async def set(self, key: str, value):
        key = f"cache:{key}"
        await self.client.setex(name=key, time=self.cache_ttl, value=value)
