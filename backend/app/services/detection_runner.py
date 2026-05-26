"""Shared detection runner — used by detection and camera API endpoints."""
import time
import uuid
from pathlib import Path
from typing import Tuple, List, Any

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from app.config import settings
from app.services.detection_service import detection_service

CLASS_COLORS = {
    "crazing": (0, 0, 255),
    "inclusion": (255, 0, 255),
    "patches": (0, 215, 255),
    "pitted_surface": (255, 0, 0),
    "rolled-in_scale": (0, 165, 255),
    "scratches": (0, 255, 0),
}

CLASS_THRESHOLDS = {
    "crazing": 0.12,
    "rolled-in_scale": 0.18,
    "inclusion": 0.20,
    "scratches": 0.25,
    "patches": 0.30,
    "pitted_surface": 0.30,
}


def _load_font() -> ImageFont.FreeTypeFont:
    font_path = settings.font_path
    try:
        return ImageFont.truetype(font_path, 16)
    except Exception:
        return ImageFont.load_default()


def run_detection(image_path: str, output_prefix: str = "result") -> Tuple[List[dict], str, float]:
    start_time = time.time()

    results = detection_service.model.predict(source=image_path, conf=0.05, iou=0.35, save=False)

    boxes = []
    for result in results:
        for box in result.boxes:
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = detection_service.get_class_name(class_id)
            min_conf = CLASS_THRESHOLDS.get(class_name, 0.30)
            if confidence < min_conf:
                continue
            chinese_name = detection_service.get_class_chinese_name(class_id, class_name)
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            boxes.append({
                "class_name": class_name, "chinese_name": chinese_name,
                "confidence": round(confidence, 3),
                "bbox": [x1, y1, x2, y2],
            })

    img = cv2.imread(image_path)
    if img is None:
        img = cv2.cvtColor(results[0].orig_img, cv2.COLOR_RGB2BGR)

    for box_info in boxes:
        x1, y1, x2, y2 = map(int, box_info["bbox"])
        color = CLASS_COLORS.get(box_info["class_name"], (0, 255, 255))
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    if boxes:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        draw = ImageDraw.Draw(pil_img)
        font = _load_font()
        for box_info in boxes:
            x1, y1 = int(box_info["bbox"][0]), int(box_info["bbox"][1])
            color_rgb = CLASS_COLORS.get(box_info["class_name"], (255, 255, 0))
            label = f" {box_info['chinese_name']} {box_info['confidence']:.2f} "
            bbox = draw.textbbox((x1, y1 - 22), label, font=font)
            draw.rectangle(bbox, fill=color_rgb)
            draw.text((x1, y1 - 22), label, fill=(255, 255, 255), font=font)
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    filename = f"{output_prefix}_{uuid.uuid4().hex}.jpg"
    filepath = Path(settings.static_dir) / filename
    cv2.imwrite(str(filepath), img)
    detection_time = round(time.time() - start_time, 3)
    result_url = f"/static/{filename}"

    return boxes, result_url, detection_time
