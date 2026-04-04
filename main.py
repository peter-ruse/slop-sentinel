import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes.analysis import analysis_router
from api.routes.auth import auth_router
from api.routes.ingestion import ingestion_router
from database.database import Database, init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Database()
    await db.connect()
    await init_db()
    yield
    await db.disconnect()


app = FastAPI(
    title="Slop Sentinel",
    swagger_ui_parameters={"displayRequestDuration": True},
    lifespan=lifespan,
    docs_url="/",
)
app.include_router(ingestion_router)
app.include_router(analysis_router)
app.include_router(auth_router)
