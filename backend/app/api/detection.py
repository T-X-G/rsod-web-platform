"""Detection APIs for the YOLO11 FastAPI backend."""

from __future__ import annotations

import logging
import mimetypes
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, Path as ApiPath, Response, UploadFile

from app.config import settings
from app.models.schemas import (
    DetectionBox,
    HistoryItem,
    HistoryResponse,
    SingleDetectionResponse,
    TargetItem,
    TargetListResponse,
)
from app.services.detection_service import detection_service
from app.services.minio_service import minio_service
from app.utils.file_utils import (
    ensure_directories,
    extract_object_filename,
    get_file_path,
    get_proxy_file_url,
    save_upload_file,
)
from app.utils.paths import Paths
from app.utils.validation import validate_upload_payload


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/detection", tags=["detection"])
ensure_directories()


def _validation_payload(report) -> list[dict]:
    return [
        {
            "name": result.name,
            "level": result.level.value,
            "message": result.message,
            "details": result.details,
        }
        for result in report.results
    ]


def _build_detection_file_url(object_key: str | None, bucket: str) -> str:
    filename = extract_object_filename(object_key)
    return get_proxy_file_url(bucket, filename) if filename else ""


def _build_history_item(record) -> HistoryItem:
    original_filename = extract_object_filename(record.original_image_key)
    result_filename = extract_object_filename(record.result_image_key)
    return HistoryItem(
        id=str(record.id),
        image_url=_build_detection_file_url(
            record.original_image_key,
            settings.minio.original_bucket,
        ),
        result_image_url=_build_detection_file_url(
            record.result_image_key,
            settings.minio.results_bucket,
        ),
        total_objects=record.total_objects or 0,
        created_at=record.created_at,
        model_name=record.model_name or "rsod-yolo11n",
        filename=original_filename or "detection.jpg",
        status=record.status or "completed",
        type=record.type or "single",
        time=record.created_at.strftime("%Y-%m-%d %H:%M") if record.created_at else "",
        count=1,
        detected_targets=[],
    )


@router.post("/single", response_model=SingleDetectionResponse)
async def detect_single_image(
    file: UploadFile = File(...),
    model_name: str = Form("rsod-yolo11n"),
    user_id: str | None = Form(None),
):
    upload_dir = Paths.uploads()
    image_path = None

    try:
        content = await file.read()
        validation_report = validate_upload_payload(
            filename=file.filename or "",
            content_type=file.content_type,
            content=content,
            allowed_extensions=settings.allowed_upload_extensions,
            allowed_mime_types=settings.allowed_upload_mime_types,
        )
        if validation_report.errors:
            logger.warning(
                "上传图片校验失败: filename=%s errors=%s",
                file.filename,
                [result.message for result in validation_report.errors],
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "上传图片校验失败",
                    "results": _validation_payload(validation_report),
                },
            )

        filename = await save_upload_file(file, upload_dir, content=content)
        image_path = get_file_path(filename, upload_dir)
        logger.info(
            "收到单图检测请求: filename=%s user_id=%s model_name=%s",
            filename,
            user_id,
            model_name,
        )

        result = detection_service.detect_single_image(
            str(image_path),
            user_id,
            model_name,
            minio_service,
        )
        return SingleDetectionResponse(success=True, message="检测成功", data=result)
    except HTTPException:
        raise
    except FileNotFoundError:
        logger.exception("检测失败，模型文件不存在。")
        raise HTTPException(status_code=500, detail="模型文件未找到")
    except Exception as exc:
        logger.exception("单图检测失败: %s", exc)
        raise HTTPException(status_code=500, detail=f"检测失败: {exc}")
    finally:
        if image_path is not None:
            try:
                Path(image_path).unlink(missing_ok=True)
            except Exception as exc:
                logger.warning("清理临时上传文件失败: %s", exc)


@router.get("/history", response_model=HistoryResponse)
async def get_detection_history(
    page: int = 1,
    page_size: int = 10,
    user_id: str | None = None,
):
    try:
        records = detection_service.get_detection_history(
            user_id=user_id,
            limit=page_size * page,
        )
        start = (page - 1) * page_size
        end = start + page_size
        history_items = [_build_history_item(record) for record in records[start:end]]
        logger.info(
            "查询检测历史成功: page=%s page_size=%s user_id=%s returned=%s",
            page,
            page_size,
            user_id,
            len(history_items),
        )
        return HistoryResponse(
            success=True,
            message="获取成功",
            data=history_items,
            total=len(records),
        )
    except Exception as exc:
        logger.exception("获取检测历史失败: %s", exc)
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {exc}")


@router.get("/{detection_id}", response_model=SingleDetectionResponse)
async def get_detection_by_id(
    detection_id: str = ApiPath(..., description="检测记录 ID"),
):
    try:
        record = detection_service.get_detection_by_id(detection_id)
        if not record:
            raise HTTPException(status_code=404, detail="检测记录不存在")

        boxes = [
            DetectionBox(
                x1=result.x1,
                y1=result.y1,
                x2=result.x2,
                y2=result.y2,
                confidence=result.confidence,
                class_id=result.class_id,
                class_name=result.class_name,
                chinese_name=result.chinese_name,
            )
            for result in getattr(record, "results", []) or []
        ]

        from app.models.schemas import DetectionResult

        detection_result = DetectionResult(
            detection_id=str(record.id),
            image_url=_build_detection_file_url(
                record.original_image_key,
                settings.minio.original_bucket,
            ),
            result_image_url=_build_detection_file_url(
                record.result_image_key,
                settings.minio.results_bucket,
            ),
            boxes=boxes,
            total_objects=record.total_objects or 0,
            detection_time=record.detection_time or 0,
            model_name=record.model_name or "rsod-yolo11n",
            created_at=record.created_at,
        )
        return SingleDetectionResponse(
            success=True,
            message="获取成功",
            data=detection_result,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("获取检测记录失败: %s", exc)
        raise HTTPException(status_code=500, detail=f"获取检测记录失败: {exc}")


@router.delete("/{detection_id}")
async def delete_detection(
    detection_id: str = ApiPath(..., description="检测记录 ID"),
):
    try:
        success = detection_service.delete_detection(detection_id)
        if not success:
            raise HTTPException(status_code=404, detail="检测记录不存在")
        logger.info("删除检测记录成功: %s", detection_id)
        return {"success": True, "message": "删除成功"}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("删除检测记录失败: %s", exc)
        raise HTTPException(status_code=500, detail=f"删除检测记录失败: {exc}")


@router.get("/targets/list", response_model=TargetListResponse)
async def get_target_list():
    targets = [
        TargetItem(
            id=target.id,
            name=target.name,
            chinese_name=target.chinese_name,
            description=target.description,
        )
        for target in settings.target_catalog
    ]
    logger.info("返回目标类别列表: count=%s", len(targets))
    return TargetListResponse(success=True, message="获取成功", data=targets)


@router.get("/files/{bucket}/{filename}", response_class=Response)
def get_file(bucket: str, filename: str):
    try:
        response = minio_service.client.get_object(bucket, filename)
        data = response.read()
        response.close()
        response.release_conn()

        media_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        return Response(
            content=data,
            media_type=media_type,
            headers={
                "Content-Disposition": f'inline; filename="{filename}"',
                "Content-Length": str(len(data)),
            },
        )
    except Exception as exc:
        logger.exception(
            "文件代理失败: bucket=%s filename=%s error=%s",
            bucket,
            filename,
            exc,
        )
        raise HTTPException(status_code=404, detail=f"文件未找到: {exc}")
