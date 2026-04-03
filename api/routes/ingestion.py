from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from api.dependencies import rate_limit_check
from api.models import RepoRequest
from services.repo.enums import Provider
from services.repo.factory import RepoServiceFactory

ingestion_router = APIRouter(prefix="/repos", tags=["ingest"])


@ingestion_router.post("/download", dependencies=[Depends(rate_limit_check)])
async def download_repo(request: RepoRequest):
    service, repo = RepoServiceFactory.get_service_from_url(request.url)  # type: ignore
    zip_buffer = await service.download_repo_zip(repo)
    filename = f"{repo.owner}-{repo.name}.zip"
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@ingestion_router.get("/top_repos", dependencies=[Depends(rate_limit_check)])
async def get_top_repos(
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=1000,
            description="Number of top Python repos to fetch",
        ),
    ] = 100,
    provider: Annotated[
        Provider,
        Query(
            description="The version control provider you wish to query",
        ),
    ] = Provider.GITHUB,
):
    service = RepoServiceFactory.get_service_from_provider(provider)
    top_repos = await service.get_top_repos(limit)
    return top_repos
