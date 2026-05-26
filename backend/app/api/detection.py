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
from app.services.detection_runner import run_detection
from app.utils.paths import Paths

router = APIRouter(prefix="/detection", tags=["检测"])

class DetectionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class DetectionRecordResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

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

        upload_dir = Paths.uploads()
        upload_dir.mkdir(parents=True, exist_ok=True)
        temp_path = upload_dir / f"upload_{uuid.uuid4().hex}.jpg"
        image_data = await file.read()
        with open(temp_path, "wb") as f:
            f.write(image_data)

        boxes, result_image_url, detection_time = run_detection(str(temp_path), "result")

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

        upload_dir = Paths.uploads()
        upload_dir.mkdir(parents=True, exist_ok=True)
        results_list = []
        for file in files:
            temp_path = upload_dir / f"batch_upload_{uuid.uuid4().hex}.jpg"
            image_data = await file.read()
            with open(temp_path, "wb") as f:
                f.write(image_data)

            boxes, result_image_url, detection_time = run_detection(str(temp_path), "result")

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
            filepath = Paths.static() / record.result_image_url.replace("/static/", "")
            if os.path.exists(filepath):
                os.remove(filepath)
        db.delete(record)
        db.commit()
        return DetectionRecordResponse(success=True, message="删除成功")
    except Exception as e:
        db.rollback()
        return DetectionRecordResponse(success=False, message=f"删除记录失败: {str(e)}")
