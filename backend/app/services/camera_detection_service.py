"""Camera real-time detection service — singleton with thread safety and concurrency control."""
import time
import threading
from typing import Dict, Any, Optional

import numpy as np

from app.config import settings
from app.services.detection_service import detection_service


class CameraDetectionService:
    _instance: Optional["CameraDetectionService"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._status = "STOPPED"
        self._lock = threading.Lock()
        self._request_semaphore = threading.Semaphore(5)
        self._frame_count = 0
        self._fps_frame_count = 0
        self._last_fps_time = time.time()
        self._confidence_threshold = 0.5
        self._iou_threshold = 0.7
        self._model_image_size = 320
        self._initialized = True

    @property
    def is_running(self) -> bool:
        return self._status == "RUNNING"

    def detect_image(self, image: np.ndarray) -> Dict[str, Any]:
        CLASS_THRESHOLDS = {
            "crazing": 0.12, "rolled-in_scale": 0.18, "inclusion": 0.20,
            "scratches": 0.25, "patches": 0.30, "pitted_surface": 0.30,
        }
        with self._request_semaphore:
            start = time.time()
            results = detection_service.model.predict(
                source=image,
                conf=self._confidence_threshold,
                iou=self._iou_threshold,
                imgsz=self._model_image_size,
                save=False,
                verbose=False,
            )

            boxes = []
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = detection_service.get_class_name(class_id)
                    min_conf = CLASS_THRESHOLDS.get(class_name, 0.30)
                    if confidence < min_conf:
                        continue
                    chinese_name = detection_service.get_class_chinese_name(class_id, class_name)
                    boxes.append({
                        "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                        "confidence": round(confidence, 3),
                        "class_id": class_id,
                        "class_name": class_name,
                        "chinese_name": chinese_name,
                    })

            detection_time = round(time.time() - start, 3)
            self._frame_count += 1
            self._fps_frame_count += 1
            now = time.time()
            elapsed = now - self._last_fps_time
            fps = 0.0
            if elapsed >= 1.0:
                fps = round(self._fps_frame_count / elapsed, 1)
                self._fps_frame_count = 0
                self._last_fps_time = now

            return {
                "boxes": boxes,
                "frame_index": self._frame_count,
                "fps": fps,
                "detection_time": detection_time,
                "total_objects": len(boxes),
            }


camera_detection_service = CameraDetectionService()
