from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid

from app.models.database import get_db
from app.models import DetectionRecord, User
from app.api.auth import get_current_user
from app.services.detection_service import detection_service
from app.services.detection_runner import run_detection
from app.utils.paths import Paths

router = APIRouter(prefix="/camera", tags=["摄像头检测"])

class CameraDetectionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

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

        upload_dir = Paths.uploads()
        upload_dir.mkdir(parents=True, exist_ok=True)
        temp_path = upload_dir / f"camera_upload_{uuid.uuid4().hex}.jpg"
        image_data = await file.read()
        with open(temp_path, "wb") as f:
            f.write(image_data)

        boxes, result_image_url, detection_time = run_detection(str(temp_path), "camera_result")

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

        upload_dir = Paths.uploads()
        upload_dir.mkdir(parents=True, exist_ok=True)
        temp_path = upload_dir / f"stream_upload_{uuid.uuid4().hex}.jpg"
        image_data = await file.read()
        with open(temp_path, "wb") as f:
            f.write(image_data)

        boxes, _, _ = run_detection(str(temp_path), "stream")

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
