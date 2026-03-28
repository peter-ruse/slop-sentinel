from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import get_redis_service, get_repo_service
from api.models import RepoRequest
from core.analysis.cyclomatic_complexity.cyclomatic_complexity import (
    CyclomaticComplexityVisitor,
)
from core.analysis.lexical_diversity.lexical_diversity import LexicalDiversityVisitor
from core.analysis.models import AnalysisResults
from core.analysis.repo_analyzer import RepoAnalyzer
from core.analysis.structural_nesting.structural_nesting import StructuralNestingVisitor
from core.parsing.python_asts import get_asts
from services.cache.redis_service import RedisService
from services.repo.base import RepoService
from services.repo.models import Repo

analysis_router = APIRouter(tags=["analyze"])


@analysis_router.post("/slop_metrics")
async def get_slop_metrics(
    request: RepoRequest,
    redis_service: Annotated[RedisService, Depends(get_redis_service)],
    repo_service: Annotated[tuple[RepoService, Repo], Depends(get_repo_service)],
) -> AnalysisResults:
    if cached_data := redis_service.get(request.url):  # type: ignore (request.url is in fact a string)
        return AnalysisResults.model_validate_json(cached_data)  # type: ignore (we know this will be a str because of how we set it)

    service, repo = repo_service
    zip_buffer = await service.download_repo_zip(repo)
    trees = get_asts(zip_buffer)
    visitors = [
        LexicalDiversityVisitor(),
        CyclomaticComplexityVisitor(),
        StructuralNestingVisitor(),
    ]
    repo_analyzer = RepoAnalyzer(visitors)
    results = repo_analyzer.consolidate_results(trees)
    results = AnalysisResults(results=results)
    redis_service.set(request.url, results.model_dump_json())  # type: ignore
    return results
