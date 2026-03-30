from fastapi import HTTPException, Request, status

from api.models import RepoRequest
from services.caching.caching_service import CachingService
from services.rate_limiting.rate_limiting_service import RateLimitingService
from services.repo.base import RepoService
from services.repo.factory import RepoServiceFactory
from services.repo.models import Repo


def get_repo_service(request: RepoRequest) -> tuple[RepoService, Repo]:
    return RepoServiceFactory.get_service_from_url(request.url)  # type: ignore


def get_caching_service() -> CachingService:
    return CachingService()


async def rate_limit_check(request: Request):
    if await RateLimitingService().is_rate_limited(
        key=request.client.host, limit=30, window=60
    ):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests"
        )
