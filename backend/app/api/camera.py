from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import uuid

from app.models.database import get_db
from app.models import DetectionRecord, User
from app.api.auth import get_current_user
from app.services.detection_service import detection_service

router = APIRouter(prefix="/camera", tags=["摄像头检测"])

STATIC_DIR = Path("static")

class CameraDetectionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

def _run_detection(image_path: str, model_name: str) -> tuple:
    import time, cv2, numpy as np
    from PIL import Image, ImageDraw, ImageFont

    start_time = time.time()
    MIN_CONF = 0.05
    CLASS_THRESHOLDS = {
        "crazing": 0.12, "rolled-in_scale": 0.18, "inclusion": 0.20,
        "scratches": 0.25, "patches": 0.30, "pitted_surface": 0.30,
    }
    CLASS_COLORS = {
        "crazing": (0, 0, 255), "inclusion": (255, 0, 255), "patches": (0, 215, 255),
        "pitted_surface": (255, 0, 0), "rolled-in_scale": (0, 165, 255), "scratches": (0, 255, 0),
    }

    results = detection_service.model.predict(source=image_path, conf=MIN_CONF, iou=0.35, save=False)

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
                "bbox": [x1, y1, x2, y2]
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
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 16)
        except Exception:
            font = ImageFont.load_default()
        for box_info in boxes:
            x1, y1 = int(box_info["bbox"][0]), int(box_info["bbox"][1])
            color_rgb = CLASS_COLORS.get(box_info["class_name"], (255, 255, 0))
            label = f" {box_info['chinese_name']} {box_info['confidence']:.2f} "
            bbox = draw.textbbox((x1, y1 - 22), label, font=font)
            draw.rectangle(bbox, fill=color_rgb)
            draw.text((x1, y1 - 22), label, fill=(255, 255, 255), font=font)
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    filename = f"camera_result_{uuid.uuid4().hex}.jpg"
    filepath = STATIC_DIR / filename
    cv2.imwrite(str(filepath), img)
    detection_time = round(time.time() - start_time, 3)

    return boxes, f"/static/{filename}", detection_time

@router.post("/detect", response_model=CameraDetectionResponse)
async def camera_detect(
    file: UploadFile = File(...),
    model_name: str = "steel-defect-yolo11n",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if detection_service.model is None:
            return CameraDetectionResponse(success=False, message="模型服务未就绪")

        temp_path = STATIC_DIR / f"camera_upload_{uuid.uuid4().hex}.jpg"
        image_data = await file.read()
        with open(temp_path, "wb") as f:
            f.write(image_data)

        boxes, result_image_url, detection_time = _run_detection(str(temp_path), model_name)

        record = DetectionRecord(
            user_id=current_user.id, filename=f"camera_{uuid.uuid4().hex}.jpg",
            total_objects=len(boxes), detection_time=detection_time,
            model_name=model_name, boxes=boxes, result_image_url=result_image_url, status="completed"
        )
        db.add(record)
        db.commit()

        try:
            temp_path.unlink()
        except Exception:
            pass

        return CameraDetectionResponse(
            success=True, message="检测完成",
            data={"id": record.id, "total_objects": len(boxes), "detection_time": detection_time,
                  "model_name": model_name, "boxes": boxes, "result_image_url": result_image_url}
        )
    except Exception as e:
        db.rollback()
        return CameraDetectionResponse(success=False, message=f"检测失败: {str(e)}")

@router.post("/stream", response_model=CameraDetectionResponse)
async def camera_stream_detect(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if detection_service.model is None:
            return CameraDetectionResponse(success=False, message="模型服务未就绪")

        temp_path = STATIC_DIR / f"stream_upload_{uuid.uuid4().hex}.jpg"
        image_data = await file.read()
        with open(temp_path, "wb") as f:
            f.write(image_data)

        boxes, _, _ = _run_detection(str(temp_path), "steel-defect-yolo11n")

        try:
            temp_path.unlink()
        except Exception:
            pass

        return CameraDetectionResponse(
            success=True, message="检测完成",
            data={"total_objects": len(boxes), "boxes": boxes}
        )
    except Exception as e:
        return CameraDetectionResponse(success=False, message=f"检测失败: {str(e)}")
