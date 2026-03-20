from fastapi import APIRouter

from api.schemas import RepoRequest
from core.analysis.cyclomatic_complexity.cyclomatic_complexity import (
    CyclomaticComplexityVisitor,
)
from core.analysis.lexical_diversity.lexical_diversity import LexicalDiversityVisitor
from core.analysis.repo_analyzer import RepoAnalyzer
from core.models import Repo
from core.parsing.python_asts import get_asts
from services.factory import RepoServiceFactory

analysis_router = APIRouter(tags=["analysis"])


@analysis_router.post("/slop_metrics")
async def get_slop_metrics(request: RepoRequest):
    service, repo = RepoServiceFactory.get_service_from_url(request.url)  # type: ignore
    zip_buffer = await service.download_repo_zip(repo)
    trees = get_asts(zip_buffer)
    visitors = [LexicalDiversityVisitor(), CyclomaticComplexityVisitor()]
    repo_analyzer = RepoAnalyzer(visitors)
    return repo_analyzer.consolidate_results(trees)
