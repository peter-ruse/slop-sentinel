from api.models import RepoRequest
from services.cache.factory import CacheServiceFactory
from services.cache.redis_service import RedisService
from services.repo.base import RepoService
from services.repo.factory import RepoServiceFactory
from services.repo.models import Repo


def get_repo_service(request: RepoRequest) -> tuple[RepoService, Repo]:
    return RepoServiceFactory.get_service_from_url(request.url)  # type: ignore


def get_redis_service() -> RedisService:
    return CacheServiceFactory.get_service()
