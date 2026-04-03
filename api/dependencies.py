from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from api.exceptions import INVALID_CREDENTIALS_EXCEPTION
from api.models import RepoRequest
from core.auth import decode_access_token
from services.caching.caching_service import CachingService
from services.rate_limiting.rate_limiting_service import RateLimitingService
from services.repo.base import RepoService
from services.repo.factory import RepoServiceFactory
from services.repo.models import Repo

# Note that tokenUrl must match the login route...
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        data = decode_access_token(token)
        if (username := data.get("sub")) is None:
            raise INVALID_CREDENTIALS_EXCEPTION
        return username
    except JWTError:
        raise INVALID_CREDENTIALS_EXCEPTION


async def rate_limit_check(username: str = Depends(get_current_user)):
    if await RateLimitingService().is_rate_limited(key=username, limit=30, window=60):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests"
        )


def get_repo_service(request: RepoRequest) -> tuple[RepoService, Repo]:
    return RepoServiceFactory.get_service_from_url(request.url)  # type: ignore


def get_caching_service() -> CachingService:
    return CachingService()
