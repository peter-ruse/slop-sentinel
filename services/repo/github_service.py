import asyncio
from io import BytesIO

import httpx

from services.repo.base import RepoService
from services.repo.models import GitHubRepo


class GitHubService(RepoService[GitHubRepo]):
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, base_url: str, token: str, per_page: int, max_parallel: int):
        if self.__class__._initialized:
            return

        self.base_url = base_url
        self.per_page = per_page
        self.semaphore = asyncio.Semaphore(max_parallel)
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }

        self.__class__._initialized = True

    async def _get_top_repos_by_page(
        self, client: httpx.AsyncClient, page: int
    ) -> list[GitHubRepo]:

        params = {
            "q": "language:python stars:>1000",
            "sort": "stars",
            "order": "desc",
            "per_page": self.per_page,
            "page": page,
        }

        response = await client.get(url="/search/repositories", params=params)
        response.raise_for_status()
        return [
            GitHubRepo(
                url=item["url"],
                owner=item["owner"]["login"],
                name=item["name"],
                star_count=item["stargazers_count"],
            )
            for item in response.json().get("items", [])
        ]

    async def get_top_repos(self, limit: int) -> list[GitHubRepo]:
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers, timeout=10.0
        ) as client:
            total_pages = -(-limit // self.per_page)
            tasks = [
                self._get_top_repos_by_page(client, page)
                for page in range(1, total_pages + 1)
            ]
            results = await asyncio.gather(*tasks)
            return [github_repo for page in results for github_repo in page]

    async def download_repo_zip(self, github_repo: GitHubRepo) -> BytesIO:
        async with self.semaphore:
            async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
                response = await client.get(
                    github_repo.zipball_url, follow_redirects=True
                )
                response.raise_for_status()
                return BytesIO(response.content)
