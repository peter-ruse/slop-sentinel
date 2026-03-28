from io import BytesIO
from typing import Protocol

from services.repo.models import Repo


class RepoService[T: Repo](Protocol):
    async def get_top_repos(self, limit: int) -> list[T]: ...

    async def download_repo_zip(self, repo: T) -> BytesIO: ...
