from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
import uuid
import os

from app.models.database import get_db
from app.models import DetectionRecord, User
from app.api.auth import get_current_user
from app.services.detection_service import detection_service

router = APIRouter(prefix="/detection", tags=["检测"])

STATIC_DIR = Path("static")

class DetectionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class DetectionRecordResponse(BaseModel):
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

    filename = f"result_{uuid.uuid4().hex}.jpg"
    filepath = STATIC_DIR / filename
    cv2.imwrite(str(filepath), img)
    detection_time = round(time.time() - start_time, 3)

    return boxes, f"/static/{filename}", detection_time

@router.post("/single", response_model=DetectionResponse)
async def detect_single_image(
    file: UploadFile = File(...),
    model_name: str = Form("steel-defect-yolo11n"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if detection_service.model is None:
            return DetectionResponse(success=False, message="模型服务未就绪")

        temp_path = STATIC_DIR / f"upload_{uuid.uuid4().hex}.jpg"
        image_data = await file.read()
        with open(temp_path, "wb") as f:
            f.write(image_data)

        boxes, result_image_url, detection_time = _run_detection(str(temp_path), model_name)

        record = DetectionRecord(
            user_id=current_user.id, filename=file.filename,
            total_objects=len(boxes), detection_time=detection_time,
            model_name=model_name, boxes=boxes, result_image_url=result_image_url, status="completed"
        )
        db.add(record)
        db.commit()

        try:
            temp_path.unlink()
        except Exception:
            pass

        return DetectionResponse(
            success=True, message="检测完成",
            data={"id": record.id, "total_objects": len(boxes), "detection_time": detection_time,
                  "model_name": model_name, "boxes": boxes, "result_image_url": result_image_url}
        )
    except Exception as e:
        db.rollback()
        return DetectionResponse(success=False, message=f"检测失败: {str(e)}")

@router.post("/batch", response_model=DetectionResponse)
async def detect_batch_images(
    files: List[UploadFile] = File(...),
    model_name: str = Form("steel-defect-yolo11n"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if detection_service.model is None:
            return DetectionResponse(success=False, message="模型服务未就绪")

        results_list = []
        for file in files:
            temp_path = STATIC_DIR / f"batch_upload_{uuid.uuid4().hex}.jpg"
            image_data = await file.read()
            with open(temp_path, "wb") as f:
                f.write(image_data)

            boxes, result_image_url, detection_time = _run_detection(str(temp_path), model_name)

            record = DetectionRecord(
                user_id=current_user.id, filename=file.filename,
                total_objects=len(boxes), detection_time=detection_time,
                model_name=model_name, boxes=boxes, result_image_url=result_image_url, status="completed"
            )
            db.add(record)
            results_list.append({
                "id": record.id, "filename": file.filename, "total_objects": len(boxes),
                "detection_time": detection_time, "boxes": boxes, "result_image_url": result_image_url
            })
            try:
                temp_path.unlink()
            except Exception:
                pass

        db.commit()
        return DetectionResponse(
            success=True, message="批量检测完成",
            data={"total_files": len(results_list), "model_name": model_name, "results": results_list}
        )
    except Exception as e:
        db.rollback()
        return DetectionResponse(success=False, message=f"批量检测失败: {str(e)}")

@router.get("/history", response_model=DetectionRecordResponse)
async def get_detection_history(
    page: int = 1, limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        offset = (page - 1) * limit
        records = db.query(DetectionRecord)\
            .filter(DetectionRecord.user_id == current_user.id)\
            .order_by(DetectionRecord.created_at.desc())\
            .offset(offset).limit(limit).all()

        results = []
        for record in records:
            results.append({
                "id": record.id, "filename": record.filename,
                "total_objects": record.total_objects, "detection_time": record.detection_time,
                "result_image_url": record.result_image_url, "created_at": record.created_at.isoformat()
            })

        total = db.query(DetectionRecord).filter(DetectionRecord.user_id == current_user.id).count()
        return DetectionRecordResponse(
            success=True, message="success",
            data={"records": results, "page": page, "limit": limit, "total": total}
        )
    except Exception as e:
        return DetectionRecordResponse(success=False, message=f"获取历史记录失败: {str(e)}")

@router.get("/detail/{record_id}", response_model=DetectionRecordResponse)
async def get_detection_detail(
    record_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        record = db.query(DetectionRecord)\
            .filter(DetectionRecord.id == record_id, DetectionRecord.user_id == current_user.id).first()
        if not record:
            return DetectionRecordResponse(success=False, message="记录不存在")
        return DetectionRecordResponse(
            success=True, message="success",
            data={"id": record.id, "filename": record.filename, "total_objects": record.total_objects,
                  "detection_time": record.detection_time, "result_image_url": record.result_image_url,
                  "created_at": record.created_at.isoformat(), "boxes": record.boxes}
        )
    except Exception as e:
        return DetectionRecordResponse(success=False, message=f"获取检测详情失败: {str(e)}")

@router.delete("/{record_id}", response_model=DetectionRecordResponse)
async def delete_detection_record(
    record_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        record = db.query(DetectionRecord)\
            .filter(DetectionRecord.id == record_id, DetectionRecord.user_id == current_user.id).first()
        if not record:
            return DetectionRecordResponse(success=False, message="记录不存在")
        if record.result_image_url:
            filepath = STATIC_DIR / record.result_image_url.replace("/static/", "")
            if os.path.exists(filepath):
                os.remove(filepath)
        db.delete(record)
        db.commit()
        return DetectionRecordResponse(success=True, message="删除成功")
    except Exception as e:
        db.rollback()
        return DetectionRecordResponse(success=False, message=f"删除记录失败: {str(e)}")
