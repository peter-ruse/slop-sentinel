import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import get_caching_service, get_repo_service, rate_limit_check
from api.models import RepoRequest
from core.analysis.cyclomatic_complexity.cyclomatic_complexity import (
    CyclomaticComplexityVisitor,
)
from core.analysis.lexical_diversity.lexical_diversity import LexicalDiversityVisitor
from core.analysis.models import AnalysisResults
from core.analysis.repo_analyzer import RepoAnalyzer
from core.analysis.structural_nesting.structural_nesting import StructuralNestingVisitor
from core.parsing.python_asts import get_asts
from services.caching.caching_service import CachingService
from services.repo.base import RepoService
from services.repo.models import Repo

logger = logging.getLogger(__name__)

analysis_router = APIRouter(prefix="/analysis", tags=["analyze"])


@analysis_router.post("/slop_metrics", dependencies=[Depends(rate_limit_check)])
async def get_slop_metrics(
    request: RepoRequest,
    caching_service: Annotated[CachingService, Depends(get_caching_service)],
    repo_service: Annotated[tuple[RepoService, Repo], Depends(get_repo_service)],
) -> AnalysisResults:
    logger.info(f"Running slop analysis on {request.url}...")

    async def produce_analysis() -> str:
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
        return AnalysisResults(results=results).model_dump_json()

    result = await caching_service.get_or_set(key=request.url, func=produce_analysis)

    return AnalysisResults.model_validate_json(result)
