import logging
import sys

from fastapi import FastAPI

from api.analysis_routes import analysis_router
from api.ingestion_routes import ingestion_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

app = FastAPI(
    title="Slop Sentinel", swagger_ui_parameters={"displayRequestDuration": True}
)
app.include_router(ingestion_router)
app.include_router(analysis_router)
