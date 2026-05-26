from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid as _uuid

from app.models.database import Base

# ===== 用户认证模型 =====
class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(_uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), nullable=True)
    role = Column(String(20), default="user")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

# ===== 检测记录模型 =====
class DetectionRecord(Base):
    __tablename__ = "detection_records"

    id = Column(String(36), primary_key=True, default=lambda: str(_uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    filename = Column(String(255), nullable=False)
    total_objects = Column(Integer, default=0)
    detection_time = Column(Float, default=0.0)
    model_name = Column(String(100))
    boxes = Column(JSON, default=list)
    result_image_url = Column(String(255))
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

# ===== 目标库模型 =====
class Target(Base):
    __tablename__ = "targets"

    id = Column(String(36), primary_key=True, default=lambda: str(_uuid.uuid4()))
    name = Column(String(100), nullable=False)
    type = Column(String(50))
    description = Column(Text)
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

# ===== AI 对话模型 =====
class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    title = Column(String, default="新对话")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    conversation = relationship("Conversation", back_populates="messages")