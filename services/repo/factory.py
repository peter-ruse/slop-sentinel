from typing import Any
from urllib.parse import urlparse

from core.config import github_settings
from services.repo.base import RepoService
from services.repo.enums import Provider
from services.repo.github_service import github_service
from services.repo.models import GitHubRepo, Repo


class RepoServiceFactory:
    @classmethod
    def get_service_from_url(cls, url: str) -> tuple[RepoService[Any], Repo]:
        domain = urlparse(url).netloc.lower().removeprefix("www.")
        match domain:
            case str() if "github.com" in domain:
                github_repo = GitHubRepo.from_url(url, github_settings.api_base_url)  # type: ignore
                return github_service, github_repo
            case str() if "bitbucket.org" in domain:
                raise NotImplementedError("Bitbucket service not implemented yet")
            case str() if "gitlab.com" in domain:
                raise NotImplementedError("GitLab service not implemented yet")
            case _:
                raise ValueError(f"Unrecognized domain {domain}")

    @classmethod
    def get_service_from_provider(cls, provider: Provider) -> RepoService[Any]:
        match provider:
            case Provider.GITHUB:
                return github_service
            case Provider.BITBUCKET:
                raise NotImplementedError("Bitbucket service not implemented yet")
            case Provider.GITLAB:
                raise NotImplementedError("GitLab service not implemented yet")
            case _:
                raise ValueError(f"Unknown provider: {provider}")
