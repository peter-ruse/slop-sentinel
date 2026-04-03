from redis.asyncio import Redis

from core.config import redis_settings
from utils.meta import SingletonMeta


class RedisService(metaclass=SingletonMeta):
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = Redis(
                host=redis_settings.host,
                port=redis_settings.port,
                db=redis_settings.db,
                password=redis_settings.raw_password,
                socket_timeout=redis_settings.socket_timeout,
                socket_connect_timeout=redis_settings.socket_connect_timeout,
            )
        return self._client
