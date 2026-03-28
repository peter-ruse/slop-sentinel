from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import urlparse


class Provider(StrEnum):
    GITHUB = "github"
    BITBUCKET = "bitbucket"
    GITLAB = "gitlab"


@dataclass(frozen=True)
class Repo:
    url: str
    owner: str
    name: str
    star_count: int | None = None


@dataclass(frozen=True)
class GitHubRepo(Repo):
    @property
    def zipball_url(self):
        base = self.url.rstrip("/")
        return base if base.endswith("zipball") else f"{base}/zipball"

    @classmethod
    def from_web_url(cls, web_url: str, api_base_url: str) -> "GitHubRepo":
        parsed = urlparse(web_url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repo URL")
        owner, name, *_ = path_parts
        name = name.removesuffix(".git")
        return cls(url=f"{api_base_url}/repos/{owner}/{name}", owner=owner, name=name)
