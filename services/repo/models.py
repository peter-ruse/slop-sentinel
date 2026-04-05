from urllib.parse import urlparse

from pydantic import BaseModel


class Repo(BaseModel):
    url: str
    owner: str
    name: str
    star_count: int | None = None


class GitHubRepo(Repo):
    @property
    def zipball_url(self):
        base = self.url.rstrip("/")
        return base if base.endswith("zipball") else f"{base}/zipball"

    @classmethod
    def from_url(cls, url: str, api_base_url: str) -> "GitHubRepo":
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repo URL")
        *_, owner, name = path_parts
        name = name.removesuffix(".git")
        return cls(url=f"{api_base_url}/repos/{owner}/{name}", owner=owner, name=name)
