import base64
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import cv2
import numpy as np

from app.api.auth import get_current_user
from app.models import User
from app.services.camera_detection_service import camera_detection_service

router = APIRouter(prefix="/camera", tags=["摄像头检测"])

class FrameRequest(BaseModel):
    image: str

class CameraDetectionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

def _decode_frame(image_data: str) -> np.ndarray:
    if "," in image_data:
        image_data = image_data.split(",", 1)[1]
    image_bytes = base64.b64decode(image_data)
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("图像解码失败")
    return image

@router.post("/detect", response_model=CameraDetectionResponse)
async def camera_detect(
    request: FrameRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        if not camera_detection_service.is_running:
            camera_detection_service._status = "RUNNING"
        image = _decode_frame(request.image)
        result = camera_detection_service.detect_image(image)
        return CameraDetectionResponse(success=True, message="检测成功", data=result)
    except ValueError as e:
        return CameraDetectionResponse(success=False, message=str(e))
    except Exception as e:
        return CameraDetectionResponse(success=False, message=f"检测失败: {str(e)}")

@router.post("/stream", response_model=CameraDetectionResponse)
async def camera_stream_detect(
    request: FrameRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        image = _decode_frame(request.image)
        result = camera_detection_service.detect_image(image)
        return CameraDetectionResponse(success=True, message="检测成功", data=result)
    except Exception as e:
        return CameraDetectionResponse(success=False, message=f"检测失败: {str(e)}")
