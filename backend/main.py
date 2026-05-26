"""FastAPI application entrypoint for the YOLO11 backend."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.utils.logging_utils import setup_app_logging
from app.utils.paths import Paths

setup_app_logging(
    level="DEBUG" if settings.debug else "INFO",
    log_file="app.log",
    use_colors=settings.debug,
)
logger = logging.getLogger(__name__)
Paths.init_runtime_dirs()
from app.models.database import init_db
init_db()

from app.api.detection import router as detection_router  # noqa: E402
from app.api.model import router as model_router  # noqa: E402
from app.api import router as qa_router  # noqa: E402
from app.api.auth import router as auth_router  # noqa: E402
from app.api.targets import router as targets_router  # noqa: E402
from app.api.camera import router as camera_router  # noqa: E402


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="YOLO11 缺陷检测平台后端 API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
app.include_router(detection_router, prefix="/api")
app.include_router(model_router, prefix="/api")
app.include_router(qa_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(targets_router, prefix="/api")
app.include_router(camera_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Check the status of local runtime paths and backend dependencies."""
    postgres_ok = False
    minio_ok = False
    redis_ok = False
    train_root_ok = False

    try:
        from sqlalchemy import text

        from app.models.database import engine

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        postgres_ok = True
    except Exception as exc:
        logger.warning("PostgreSQL health check failed: %s", exc)

    try:
        from app.services.redis_service import redis_service

        redis_ok = bool(redis_service.ping())
        if not redis_ok:
            logger.warning("Redis health check returned an unhealthy status.")
    except Exception as exc:
        logger.warning("Redis health check failed: %s", exc)

    try:
        from app.services.minio_service import minio_service

        minio_service.client.list_buckets()
        minio_ok = True
    except Exception as exc:
        logger.warning("MinIO health check failed: %s", exc)

    try:
        train_root = Paths.train_root()
        train_root_ok = train_root.exists() and train_root.is_dir()
        if not train_root_ok:
            logger.warning("Configured train root is unavailable: %s", train_root)
    except Exception as exc:
        logger.warning("Dataset path health check failed: %s", exc)

    all_ok = all([postgres_ok, minio_ok, redis_ok, train_root_ok])
    return {
        "status": "healthy" if all_ok else "degraded",
        "services": {
            "postgres": "up" if postgres_ok else "down",
            "minio": "up" if minio_ok else "down",
            "redis": "up" if redis_ok else "down",
            "dataset": "up" if train_root_ok else "down",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
        access_log=True,
    )
