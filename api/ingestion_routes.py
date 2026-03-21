from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from api.schemas import RepoRequest
from services.factory import RepoServiceFactory
from services.models import Provider

ingestion_router = APIRouter(tags=["ingest"])


@ingestion_router.post("/download")
async def download_repo(request: RepoRequest):
    service, repo = RepoServiceFactory.get_service_from_url(request.url)  # type: ignore
    zip_buffer = await service.download_repo_zip(repo)
    filename = f"{repo.owner}-{repo.name}.zip"
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@ingestion_router.get("/top_repos")
async def get_top_repos(
    limit: int = Query(
        default=100,
        ge=1,
        le=10000,
        description="Number of top Python repos to fetch",
    ),
    provider: Provider = Query(
        default=Provider.GITHUB,
        description="The version control provider you wish to query",
    ),
):
    service = RepoServiceFactory.get_service_from_provider(provider)
    top_repos = await service.get_top_repos(limit)
    return top_repos
