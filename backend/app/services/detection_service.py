"""YOLO11 detection service used by the FastAPI backend."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

from app.config import settings
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
        if not os.path.exists(settings.yolo_model_path):
            raise FileNotFoundError(f"模型文件未找到: {settings.yolo_model_path}")
        self.model = YOLO(settings.yolo_model_path)
        logger.info("模型加载成功: %s", settings.yolo_model_path)

    def reload_model(self, model_object_name: Optional[str] = None) -> bool:
        try:
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


detection_service = DetectionService()
