from typing import Any, Callable, Coroutine

from services.redis_service import RedisService
from utils.meta import SingletonMeta


class CachingService(metaclass=SingletonMeta):
    def __init__(self, prefix: str = "cache"):
        self.redis_service = RedisService()
        self.prefix = prefix

    @property
    def client(self):
        return self.redis_service.client

    def _make_full_key(self, key: str):
        return f"{self.prefix}:{key}"

    async def get(self, key: str):
        full_key = self._make_full_key(key)
        return await self.client.get(full_key)

    async def set(self, key: str, value, cache_ttl: int):
        full_key = self._make_full_key(key)
        await self.client.setex(name=full_key, time=cache_ttl, value=value)

    async def get_or_set(
        self, key, func: Callable[[], Coroutine[Any, Any, str]], cache_ttl: int = 3600
    ) -> str:
        full_key = self._make_full_key(key)

        if cached_data := await self.get(full_key):
            return cached_data

        result = await func()
        await self.set(key=full_key, value=result, cache_ttl=cache_ttl)
        return result
