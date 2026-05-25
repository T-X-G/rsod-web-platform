"""Model management APIs for the YOLO11 backend."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from app.config import settings
from app.models.schemas import (
    CurrentModelResponse,
    ModelItem,
    ModelListResponse,
    ModelMetadata,
    ReloadModelRequest,
    ReloadModelResponse,
)
from app.services.detection_service import detection_service
from app.services.minio_service import minio_service


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/model", tags=["model"])


def _build_model_metadata(raw_metadata):
    if not raw_metadata:
        return None
    return ModelMetadata(
        name=raw_metadata.get("name", "unknown"),
        version=raw_metadata.get("version", "unknown"),
        created_at=raw_metadata.get("created_at"),
        description=raw_metadata.get("description"),
        metrics=raw_metadata.get("metrics"),
        config=raw_metadata.get("config"),
    )


def _build_model_item(object_name: str, metadata) -> ModelItem:
    public_url = ""
    if object_name and object_name != "unknown":
        public_url = minio_service.get_public_url(settings.minio.models_bucket, object_name)
    return ModelItem(
        object_name=object_name,
        metadata=_build_model_metadata(metadata),
        public_url=public_url,
    )


@router.get("/list", response_model=ModelListResponse)
async def get_model_list():
    try:
        models_with_meta = minio_service.list_models_with_metadata()
        model_items = [
            _build_model_item(model["object_name"], model.get("metadata"))
            for model in models_with_meta
        ]

        latest_model = None
        latest_object_name = minio_service.get_latest_model()
        if latest_object_name:
            latest_model = next(
                (item for item in model_items if item.object_name == latest_object_name),
                None,
            )

        logger.info("获取模型列表成功: count=%s", len(model_items))
        return ModelListResponse(
            success=True,
            message="获取成功",
            data=model_items,
            latest=latest_model,
        )
    except Exception as exc:
        logger.exception("获取模型列表失败: %s", exc)
        raise HTTPException(status_code=500, detail=f"获取模型列表失败: {exc}")


@router.get("/current", response_model=CurrentModelResponse)
async def get_current_model():
    try:
        current_info = detection_service.current_model_info
        model_item = _build_model_item(
            current_info.get("object_name", "unknown"),
            current_info.get("metadata"),
        )
        logger.info("获取当前模型成功: object_name=%s", model_item.object_name)
        return CurrentModelResponse(
            success=True,
            message="获取成功",
            data=model_item,
        )
    except Exception as exc:
        logger.exception("获取当前模型信息失败: %s", exc)
        raise HTTPException(status_code=500, detail=f"获取当前模型信息失败: {exc}")


@router.post("/reload", response_model=ReloadModelResponse)
async def reload_model(request: ReloadModelRequest | None = None):
    try:
        target_object_name = request.object_name if request else None
        success = detection_service.reload_model(model_object_name=target_object_name)
        if not success:
            raise HTTPException(status_code=500, detail="模型重新加载失败")

        current_info = detection_service.current_model_info
        model_item = _build_model_item(
            current_info.get("object_name", "unknown"),
            current_info.get("metadata"),
        )
        logger.info("模型重新加载成功: object_name=%s", model_item.object_name)
        return ReloadModelResponse(
            success=True,
            message="模型重新加载成功",
            data=model_item,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("模型重新加载失败: %s", exc)
        raise HTTPException(status_code=500, detail=f"模型重新加载失败: {exc}")
