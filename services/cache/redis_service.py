from redis import Redis


class RedisService:
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        password: str,
        cache_ttl: int,
    ):
        self.client = Redis(host=host, port=port, db=db, password=password)
        self.cache_ttl = cache_ttl

    def get(self, name: str):
        return self.client.get(name)

    def set(self, name: str, value: str):
        self.client.setex(name=name, time=self.cache_ttl, value=value)
