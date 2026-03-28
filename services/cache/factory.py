from core.config import RedisSettings
from services.cache.redis_service import RedisService


class CacheServiceFactory:
    _instance = None

    @classmethod
    def get_service(cls) -> RedisService:
        settings = RedisSettings()  # type: ignore
        if not cls._instance:
            cls._instance = RedisService(
                host=settings.host,
                port=settings.port,
                db=settings.db,
                password=settings.raw_password,
                cache_ttl=settings.cache_ttl,
            )
        return cls._instance
