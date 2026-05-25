"""YOLO11 detection service used by the FastAPI backend."""

from __future__ import annotations

import logging
import os
import time
import uuid
from datetime import datetime
import json
from pathlib import Path
from typing import List, Optional

import cv2
from ultralytics import YOLO

from app.config import settings
from app.models.database import (
    DetectionRecord,
    DetectionResult as DBDetectionResult,
    SessionLocal,
)
from app.models.schemas import DetectionBox, DetectionResult
from app.services.minio_service import minio_service
from app.utils.file_utils import get_proxy_file_url
from app.utils.paths import Paths


logger = logging.getLogger(__name__)


class DetectionService:
    """Encapsulate YOLO11 model loading, inference, and persistence."""

    def __init__(self) -> None:
        self.model: Optional[YOLO] = None
        self.current_model_info = {
            "version": None,
            "object_name": None,
            "loaded_at": None,
            "metadata": None,
        }
        self.local_model_info_path = Paths.models() / "model_info.json"
        self.class_names = {target.id: target.name for target in settings.target_catalog}
        self.class_labels = {
            target.name: target.chinese_name for target in settings.target_catalog
        }
        self._load_model_smart()

    def _save_local_model_info(self, model_info: dict) -> None:
        try:
            info_path = Paths.ensure_dir(self.local_model_info_path.parent) / self.local_model_info_path.name
            info_path.write_text(json.dumps(model_info, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as exc:
            logger.warning("保存本地模型信息失败: %s", exc)

    def _load_local_model_info(self) -> Optional[dict]:
        try:
            if not self.local_model_info_path.exists():
                return None
            return json.loads(self.local_model_info_path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("加载本地模型信息失败: %s", exc)
            return None

    def _load_model_smart(self) -> None:
        local_info = self._load_local_model_info()
        latest_model = minio_service.get_latest_model()
        need_download = False
        model_object_name = None

        if not os.path.exists(settings.yolo_model_path):
            logger.info("本地模型不存在，需要从 MinIO 下载。")
            need_download = True
        elif not local_info:
            logger.info("本地模型缺少版本信息，检查 MinIO 最新版本。")
            need_download = True
        elif latest_model and local_info.get("object_name") != latest_model:
            logger.info(
                "发现新版本模型 %s，当前版本为 %s。",
                latest_model,
                local_info.get("object_name", "unknown"),
            )
            need_download = True
        elif latest_model:
            logger.info("本地模型已是最新版本: %s", latest_model)

        if need_download and latest_model:
            logger.info("开始下载最新模型: %s", latest_model)
            success = minio_service.download_model_file(
                latest_model,
                settings.yolo_model_path,
            )
            if success:
                model_object_name = latest_model
                logger.info("模型下载成功: %s", settings.yolo_model_path)
            elif os.path.exists(settings.yolo_model_path):
                logger.warning("模型下载失败，继续使用本地模型: %s", settings.yolo_model_path)
                model_object_name = local_info.get("object_name") if local_info else None
            else:
                raise FileNotFoundError(f"模型下载失败且本地不存在: {latest_model}")
        elif not latest_model:
            if not os.path.exists(settings.yolo_model_path):
                raise FileNotFoundError(f"模型文件未找到: {settings.yolo_model_path}")
            model_object_name = local_info.get("object_name") if local_info else None
        else:
            model_object_name = local_info.get("object_name") if local_info else None

        self.model = YOLO(settings.yolo_model_path)
        model_metadata = (
            minio_service.get_model_metadata(model_object_name)
            if model_object_name
            else None
        )
        self.current_model_info = {
            "version": model_metadata.get("version", "unknown")
            if model_metadata
            else "unknown",
            "object_name": model_object_name,
            "loaded_at": datetime.now().isoformat(),
            "metadata": model_metadata,
        }
        self._save_local_model_info(self.current_model_info)
        logger.info(
            "模型加载成功: %s (版本: %s)",
            settings.yolo_model_path,
            self.current_model_info["version"],
        )

    def reload_model(self, model_object_name: Optional[str] = None) -> bool:
        try:
            if model_object_name:
                logger.info("准备加载指定模型: %s", model_object_name)
                success = minio_service.download_model_file(
                    model_object_name,
                    settings.yolo_model_path,
                )
                if not success:
                    logger.error("指定模型下载失败: %s", model_object_name)
                    return False
            else:
                logger.info("准备重新加载最新模型。")

            self.model = None
            self._load_model_smart()
            return True
        except Exception as exc:
            logger.error("重新加载模型失败: %s", exc, exc_info=True)
            return False

    def get_class_name(self, class_id: int) -> str:
        if class_id in self.class_names:
            return self.class_names[class_id]
        if self.model and hasattr(self.model, "names") and class_id in self.model.names:
            return str(self.model.names[class_id])
        return f"class_{class_id}"

    def get_class_chinese_name(self, class_id: int, class_name: str) -> str:
        target = settings.get_target_by_id(class_id)
        if target:
            return target.chinese_name
        return self.class_labels.get(class_name, class_name)

    def detect_single_image(
        self,
        image_path: str,
        user_id: Optional[str] = None,
        model_name: str = "rsod-yolo11n",
        minio_svc=None,
    ) -> DetectionResult:
        if self.model is None:
            raise RuntimeError("YOLO 模型尚未完成初始化。")

        start_time = time.time()
        detection_id = str(uuid.uuid4())
        logger.info("开始单图检测: detection_id=%s image=%s", detection_id, image_path)

        results = self.model.predict(
            source=image_path,
            conf=settings.confidence_threshold,
            iou=settings.iou_threshold,
            save=False,
        )

        boxes: List[DetectionBox] = []
        db_results: List[DBDetectionResult] = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = self.get_class_name(class_id)
                chinese_name = self.get_class_chinese_name(class_id, class_name)

                boxes.append(
                    DetectionBox(
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                        confidence=confidence,
                        class_id=class_id,
                        class_name=class_name,
                        chinese_name=chinese_name,
                    )
                )
                db_results.append(
                    DBDetectionResult(
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                        confidence=confidence,
                        class_id=class_id,
                        class_name=class_name,
                        chinese_name=chinese_name,
                    )
                )

        annotated_image = results[0].plot()
        annotated_image_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
        _, encoded_image = cv2.imencode(".jpg", annotated_image_bgr)
        result_image_bytes = encoded_image.tobytes()

        minio_client = minio_svc if minio_svc is not None else minio_service
        result_object_name = minio_client.upload_result_image(result_image_bytes, "jpg")

        image_filename = Path(image_path).name
        original_image_bytes = Path(image_path).read_bytes()
        original_object_name = minio_client.upload_image_bytes(
            original_image_bytes,
            image_filename,
        )

        detection_time = time.time() - start_time
        original_image_key = f"uploads/{original_object_name}"
        result_image_key = f"results/{result_object_name}"

        self._save_to_database(
            user_id=user_id,
            detection_id=detection_id,
            model_name=model_name,
            total_objects=len(boxes),
            detection_time=detection_time,
            original_image_key=original_image_key,
            result_image_key=result_image_key,
            results=db_results,
        )

        logger.info(
            "单图检测完成: detection_id=%s total_objects=%s elapsed=%.3fs",
            detection_id,
            len(boxes),
            detection_time,
        )
        return DetectionResult(
            detection_id=detection_id,
            image_url=get_proxy_file_url(settings.minio.original_bucket, original_object_name),
            result_image_url=get_proxy_file_url(
                settings.minio.results_bucket,
                result_object_name,
            ),
            boxes=boxes,
            total_objects=len(boxes),
            detection_time=round(detection_time, 3),
            model_name=model_name,
            created_at=datetime.now(),
        )

    def _save_to_database(
        self,
        user_id: Optional[str],
        detection_id: str,
        model_name: str,
        total_objects: int,
        detection_time: float,
        original_image_key: str,
        result_image_key: str,
        results: List[DBDetectionResult],
    ) -> Optional[DetectionRecord]:
        try:
            with SessionLocal() as db:
                record = DetectionRecord(
                    id=detection_id,
                    user_id=user_id,
                    type="single",
                    status="completed",
                    model_name=model_name,
                    model_version=str(self.current_model_info.get("version") or "unknown"),
                    total_objects=total_objects,
                    detection_time=detection_time,
                    original_image_key=original_image_key,
                    result_image_key=result_image_key,
                )
                db.add(record)
                for result in results:
                    result.record_id = detection_id
                    db.add(result)
                db.commit()
                db.refresh(record)
                logger.info("检测记录已保存到数据库: %s", detection_id)
                return record
        except Exception as exc:
            logger.error("保存检测记录到数据库失败: %s", exc, exc_info=True)
            return None

    def get_detection_history(
        self,
        user_id: Optional[str] = None,
        limit: int = 10,
    ) -> List[DetectionRecord]:
        try:
            with SessionLocal() as db:
                query = db.query(DetectionRecord).order_by(DetectionRecord.created_at.desc())
                if user_id:
                    query = query.filter(DetectionRecord.user_id == user_id)
                records = query.limit(limit).all()
                logger.info("获取检测历史记录成功: count=%s user_id=%s", len(records), user_id)
                return records
        except Exception as exc:
            logger.error("获取检测历史记录失败: %s", exc, exc_info=True)
            return []

    def get_detection_by_id(self, detection_id: str) -> Optional[DetectionRecord]:
        try:
            with SessionLocal() as db:
                record = (
                    db.query(DetectionRecord)
                    .filter(DetectionRecord.id == detection_id)
                    .first()
                )
                if record:
                    _ = record.results
                    logger.info("获取检测记录成功: %s", detection_id)
                else:
                    logger.warning("检测记录不存在: %s", detection_id)
                return record
        except Exception as exc:
            logger.error("获取检测记录失败: %s", exc, exc_info=True)
            return None

    def delete_detection(self, detection_id: str) -> bool:
        try:
            with SessionLocal() as db:
                record = (
                    db.query(DetectionRecord)
                    .filter(DetectionRecord.id == detection_id)
                    .first()
                )
                if record is None:
                    logger.warning("检测记录不存在: %s", detection_id)
                    return False

                db.query(DBDetectionResult).filter(
                    DBDetectionResult.record_id == detection_id
                ).delete()
                db.delete(record)
                db.commit()
                logger.info("检测记录已删除: %s", detection_id)
                return True
        except Exception as exc:
            logger.error("删除检测记录失败: %s", exc, exc_info=True)
            return False


detection_service = DetectionService()
