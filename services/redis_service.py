from redis.asyncio import Redis

from core.config import RedisSettings


class RedisService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.__class__._initialized:
            return

        settings = RedisSettings()  # type: ignore
        self.client = Redis(
            host=settings.host,
            port=settings.port,
            db=settings.db,
            password=settings.raw_password,
        )

        self.__class__._initialized = True
