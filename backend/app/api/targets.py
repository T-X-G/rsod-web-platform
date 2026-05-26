from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.models.database import get_db
from app.models import Target, User
from app.api.auth import get_current_user

import uuid
import os
from pathlib import Path

router = APIRouter(prefix="/targets", tags=["目标库"])

STATIC_DIR = Path("static")

class TargetResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

@router.post("/", response_model=TargetResponse)
async def create_target(
    name: str = Form(...),
    type: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        image_url = None
        if image:
            filename = f"target_{uuid.uuid4().hex}.jpg"
            filepath = STATIC_DIR / filename
            image_data = await image.read()
            with open(filepath, "wb") as f:
                f.write(image_data)
            image_url = f"/static/{filename}"

        target = Target(name=name, type=type, description=description, image_url=image_url)
        db.add(target)
        db.commit()
        db.refresh(target)

        return TargetResponse(
            success=True, message="创建成功",
            data={"id": target.id, "name": target.name, "type": target.type,
                  "description": target.description, "image_url": target.image_url,
                  "created_at": target.created_at.isoformat()}
        )
    except Exception as e:
        db.rollback()
        return TargetResponse(success=False, message=f"创建失败: {str(e)}")

@router.get("/", response_model=TargetResponse)
@router.get("/list", response_model=TargetResponse)
async def get_targets(
    page: int = 1, limit: int = 10, type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        offset = (page - 1) * limit
        query = db.query(Target)
        if type:
            query = query.filter(Target.type == type)
        targets = query.order_by(Target.created_at.desc()).offset(offset).limit(limit).all()

        results = []
        for target in targets:
            results.append({
                "id": target.id, "name": target.name, "type": target.type,
                "description": target.description, "image_url": target.image_url,
                "created_at": target.created_at.isoformat()
            })
        total = query.count()
        return TargetResponse(success=True, message="success",
                              data={"targets": results, "page": page, "limit": limit, "total": total})
    except Exception as e:
        return TargetResponse(success=False, message=f"获取失败: {str(e)}")

@router.get("/{target_id}", response_model=TargetResponse)
async def get_target(target_id: str, db: Session = Depends(get_db)):
    try:
        target = db.query(Target).filter(Target.id == target_id).first()
        if not target:
            return TargetResponse(success=False, message="目标不存在")
        return TargetResponse(success=True, message="success",
                              data={"id": target.id, "name": target.name, "type": target.type,
                                    "description": target.description, "image_url": target.image_url,
                                    "created_at": target.created_at.isoformat(),
                                    "updated_at": target.updated_at.isoformat()})
    except Exception as e:
        return TargetResponse(success=False, message=f"获取失败: {str(e)}")

@router.put("/{target_id}", response_model=TargetResponse)
async def update_target(
    target_id: str, name: Optional[str] = Form(None), type: Optional[str] = Form(None),
    description: Optional[str] = Form(None), image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        target = db.query(Target).filter(Target.id == target_id).first()
        if not target:
            return TargetResponse(success=False, message="目标不存在")
        if name: target.name = name
        if type: target.type = type
        if description: target.description = description
        if image:
            if target.image_url:
                old_filepath = STATIC_DIR / target.image_url.replace("/static/", "")
                if os.path.exists(old_filepath):
                    os.remove(old_filepath)
            filename = f"target_{uuid.uuid4().hex}.jpg"
            filepath = STATIC_DIR / filename
            image_data = await image.read()
            with open(filepath, "wb") as f:
                f.write(image_data)
            target.image_url = f"/static/{filename}"
        db.commit()
        db.refresh(target)
        return TargetResponse(success=True, message="更新成功",
                              data={"id": target.id, "name": target.name, "type": target.type,
                                    "description": target.description, "image_url": target.image_url,
                                    "updated_at": target.updated_at.isoformat()})
    except Exception as e:
        db.rollback()
        return TargetResponse(success=False, message=f"更新失败: {str(e)}")

@router.delete("/{target_id}", response_model=TargetResponse)
async def delete_target(
    target_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        target = db.query(Target).filter(Target.id == target_id).first()
        if not target:
            return TargetResponse(success=False, message="目标不存在")
        if target.image_url:
            filepath = STATIC_DIR / target.image_url.replace("/static/", "")
            if os.path.exists(filepath):
                os.remove(filepath)
        db.delete(target)
        db.commit()
        return TargetResponse(success=True, message="删除成功")
    except Exception as e:
        db.rollback()
        return TargetResponse(success=False, message=f"删除失败: {str(e)}")
