import ast
from io import BytesIO
from typing import Protocol

from core.models import MetricName, Repo


class RepoService[T: Repo](Protocol):
    async def get_top_repos(self, limit: int) -> list[T]: ...

    async def download_repo_zip(self, repo: T) -> BytesIO: ...


class MetricVisitor(Protocol):
    metric_name: MetricName

    def update_module_fqn(self, module_fqn: str): ...

    def visit(self, tree: ast.AST): ...

    def compute_results(self): ...
