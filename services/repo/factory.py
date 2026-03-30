from typing import Any
from urllib.parse import urlparse

from core.config import GitHubSettings
from services.repo.base import RepoService
from services.repo.github_service import GitHubService
from services.repo.models import GitHubRepo, Provider, Repo


class RepoServiceFactory:
    @classmethod
    def get_service_from_url(cls, url: str) -> tuple[RepoService[Any], Repo]:
        domain = urlparse(url).netloc.lower().removeprefix("www.")
        match domain:
            case "github.com":
                settings = GitHubSettings()  # type: ignore
                github_repo = GitHubRepo.from_web_url(url, settings.api_base_url)  # type: ignore
                github_service = GitHubService(
                    base_url=settings.api_base_url,  # type: ignore
                    token=settings.raw_token,
                    per_page=settings.per_page,
                    max_parallel=settings.max_parallel,
                )
                return github_service, github_repo
            case "bitbucket.org":
                raise NotImplementedError("Bitbucket service not implemented yet")
            case "gitlab.com":
                raise NotImplementedError("GitLab service not implemented yet")
            case _:
                raise ValueError(f"Unrecognized domain {domain}")

    @classmethod
    def get_service_from_provider(cls, provider: Provider) -> RepoService[Any]:
        match provider:
            case Provider.GITHUB:
                settings = GitHubSettings()  # type: ignore
                return GitHubService(
                    base_url=settings.api_base_url,  # type: ignore
                    token=settings.raw_token,
                    per_page=settings.per_page,
                    max_parallel=settings.max_parallel,
                )
            case Provider.BITBUCKET:
                raise NotImplementedError("Bitbucket service not implemented yet")
            case Provider.GITLAB:
                raise NotImplementedError("GitLab service not implemented yet")
            case _:
                raise ValueError(f"Unknown provider: {provider}")
