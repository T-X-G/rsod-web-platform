"""Video detection API endpoints for real-time frame and full video processing."""
import base64
import os
import threading
import time
import uuid
from pathlib import Path
from typing import Dict, Any

import cv2
import numpy as np
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.api.auth import get_current_user
from app.config import settings
from app.models import User
from app.services.camera_detection_service import camera_detection_service
from app.services.detection_service import detection_service

router = APIRouter(prefix="/video-detection", tags=["视频检测"])

MAX_VIDEO_SIZE = 200 * 1024 * 1024
_tasks: Dict[str, dict] = {}
_task_lock = threading.Lock()

CLASS_THRESHOLDS = {
    "crazing": 0.12, "rolled-in_scale": 0.18, "inclusion": 0.20,
    "scratches": 0.25, "patches": 0.30, "pitted_surface": 0.30,
}


class FrameResponse(dict):
    success: bool
    message: str
    data: dict | None


@router.post("/info")
async def get_video_info(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if file.size and file.size > MAX_VIDEO_SIZE:
        raise HTTPException(413, "视频文件超过 200MB 限制")
    temp_path = Path(settings.static_dir) / f"video_tmp_{uuid.uuid4().hex}{Path(file.filename or '.mp4').suffix}"
    try:
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        cap = cv2.VideoCapture(str(temp_path))
        try:
            if not cap.isOpened():
                return {"success": False, "message": "无法解码视频，编码格式不支持"}
            return {
                "success": True,
                "data": {
                    "fps": cap.get(cv2.CAP_PROP_FPS),
                    "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                    "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                    "duration": cap.get(cv2.CAP_PROP_FRAME_COUNT) / max(cap.get(cv2.CAP_PROP_FPS), 1),
                }
            }
        finally:
            cap.release()
    except Exception as e:
        return {"success": False, "message": f"读取视频信息失败: {str(e)}"}
    finally:
        try: temp_path.unlink()
        except Exception: pass


@router.post("/realtime-frame")
async def detect_realtime_frame(
    file: UploadFile = File(...),
    confidence_threshold: float = Form(0.25),
    iou_threshold: float = Form(0.7),
    current_user: User = Depends(get_current_user),
):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            return {"success": False, "message": "无法解码图片"}
        return {"success": True, "data": _detect(frame=image, conf=confidence_threshold, iou=iou_threshold)}
    except Exception as e:
        return {"success": False, "message": f"帧检测失败: {str(e)}"}


def _detect(frame: np.ndarray, conf: float, iou: float) -> dict:
    results = detection_service.model.predict(source=frame, conf=conf, iou=iou, save=False, verbose=False)
    boxes = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cf = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = detection_service.get_class_name(class_id)
            min_cf = CLASS_THRESHOLDS.get(class_name, 0.30)
            if cf < min_cf:
                continue
            boxes.append({
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "confidence": round(cf, 3), "class_id": class_id,
                "class_name": class_name,
                "chinese_name": detection_service.get_class_chinese_name(class_id, class_name),
            })
    return {
        "boxes": boxes, "total_objects": len(boxes),
        "image_width": frame.shape[1], "image_height": frame.shape[0],
    }


@router.post("/full")
async def full_video_detection(
    file: UploadFile = File(...),
    frame_interval: int = Form(1),
    confidence_threshold: float = Form(0.25),
    iou_threshold: float = Form(0.7),
    current_user: User = Depends(get_current_user),
):
    if file.size and file.size > MAX_VIDEO_SIZE:
        raise HTTPException(413, "视频文件超过 200MB 限制")
    task_id = str(uuid.uuid4())
    temp_path = Path(settings.static_dir) / f"video_task_{task_id}{Path(file.filename or '.mp4').suffix}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    cancel_event = threading.Event()
    with _task_lock:
        _tasks[task_id] = {"status": "processing", "progress": 0, "cancel": cancel_event, "started_at": time.time()}

    threading.Thread(target=_process_video, args=(task_id, str(temp_path), frame_interval, confidence_threshold, iou_threshold, cancel_event), daemon=True).start()
    return {"success": True, "data": {"task_id": task_id}}


def _process_video(task_id: str, path: str, frame_interval: int, conf: float, iou: float, cancel_event: threading.Event):
    cap = cv2.VideoCapture(path)
    total = max(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), 1)
    processed = 0
    frames_data = []
    try:
        while True:
            if cancel_event.is_set():
                with _task_lock: _tasks[task_id]["status"] = "cancelled"
                break
            ret, frame = cap.read()
            if not ret:
                with _task_lock: _tasks[task_id]["status"] = "completed"
                break
            if processed % frame_interval == 0:
                result = _detect(frame, conf, iou)
                frames_data.append({"frame_index": processed, **result})
            processed += 1
            with _task_lock:
                if task_id in _tasks:
                    _tasks[task_id]["progress"] = processed / total
    except Exception as e:
        with _task_lock:
            if task_id in _tasks:
                _tasks[task_id]["status"] = "failed"
                _tasks[task_id]["error"] = str(e)
    finally:
        cap.release()
        try: os.remove(path)
        except Exception: pass
        with _task_lock:
            if task_id in _tasks and _tasks[task_id]["status"] == "processing":
                _tasks[task_id]["status"] = "completed"
            if task_id in _tasks:
                _tasks[task_id]["result"] = {
                    "total_frames": processed, "detected_frames": len(frames_data),
                    "frames_data": frames_data,
                }


@router.get("/progress/{task_id}")
async def get_progress(task_id: str, current_user: User = Depends(get_current_user)):
    with _task_lock:
        task = _tasks.get(task_id)
    if not task:
        return {"success": False, "message": "任务不存在或已过期"}
    return {"success": True, "data": {"status": task["status"], "progress": task.get("progress", 0)}}


@router.get("/result/{task_id}")
async def get_result(task_id: str, current_user: User = Depends(get_current_user)):
    with _task_lock:
        task = _tasks.get(task_id)
    if not task:
        return {"success": False, "message": "任务不存在或已过期"}
    if task["status"] == "processing":
        return {"success": False, "message": "视频仍在处理中"}
    return {"success": True, "data": {"status": task["status"], "result": task.get("result"), "error": task.get("error")}}


@router.post("/cancel/{task_id}")
async def cancel_detection(task_id: str, current_user: User = Depends(get_current_user)):
    with _task_lock:
        task = _tasks.get(task_id)
    if not task:
        return {"success": False, "message": "任务不存在或已过期"}
    task["cancel"].set()
    return {"success": True, "message": "已发送取消信号"}
