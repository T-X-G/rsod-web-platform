from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.services import QAService
from app.models.database import get_db
from app.services.redis_service import redis_service
from app.models import User, Conversation as DBConversation, Message as DBMessage
from app.api.auth import get_current_user
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json

router = APIRouter(prefix="/qa", tags=["AI问答"])

class MessageItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[MessageItem]
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class UpdateTitleRequest(BaseModel):
    title: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        service = QAService()
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        response_content = service.generate_response(messages)
        messages.append({"role": "assistant", "content": response_content})

        if request.conversation_id:
            conversation = db.query(DBConversation).filter(
                DBConversation.id == request.conversation_id,
                DBConversation.user_id == current_user.id
            ).first()
            if conversation:
                conversation.updated_at = datetime.now()
                db.add(DBMessage(conversation_id=conversation.id, role="assistant", content=response_content))
                db.commit()
                service.cache_conversation(request.conversation_id, messages)
        else:
            first_message = next((m for m in messages if m["role"] == "user"), None)
            title = first_message["content"][:50] if first_message else "新对话"
            conversation = DBConversation(user_id=current_user.id, title=title)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            for msg in messages:
                db.add(DBMessage(conversation_id=conversation.id, role=msg["role"], content=msg["content"]))
            db.commit()
            service.cache_conversation(conversation.id, messages)
            request.conversation_id = conversation.id

        return ChatResponse(
            success=True, message="success",
            data={"conversation_id": request.conversation_id, "response": response_content, "messages": messages}
        )
    except Exception as e:
        db.rollback()
        return ChatResponse(success=False, message=str(e))

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        service = QAService()
        messages = [{"role": m.role, "content": m.content} for m in request.messages]

        async def event_stream():
            full = ""
            try:
                for token in service.generate_stream(messages):
                    full += token
                    yield f"data: {json.dumps({'token': token, 'full': full}, ensure_ascii=False)}\n\n"
                yield f"data: {json.dumps({'done': True, 'full': full}, ensure_ascii=False)}\n\n"
            except Exception:
                yield f"data: {json.dumps({'error': True, 'full': full})}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")
    except Exception as e:
        return ChatResponse(success=False, message=str(e))

@router.get("/conversations", response_model=ChatResponse)
async def get_conversations(
    limit: int = 10, offset: int = 0,
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        conversations = db.query(DBConversation)\
            .filter(DBConversation.user_id == current_user.id)\
            .order_by(DBConversation.updated_at.desc()).offset(offset).limit(limit).all()
        result = []
        for conv in conversations:
            result.append({"id": conv.id, "title": conv.title,
                           "created_at": conv.created_at.isoformat(), "updated_at": conv.updated_at.isoformat()})
        return ChatResponse(success=True, message="success", data={"conversations": result})
    except Exception as e:
        return ChatResponse(success=False, message=str(e))

@router.get("/conversation/{conversation_id}", response_model=ChatResponse)
async def get_conversation(
    conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        service = QAService()
        cached = service.get_cached_conversation(conversation_id)
        if cached:
            return ChatResponse(success=True, message="success", data={"messages": cached})
        conversation = db.query(DBConversation)\
            .filter(DBConversation.id == conversation_id, DBConversation.user_id == current_user.id).first()
        if not conversation:
            return ChatResponse(success=False, message="对话不存在")
        messages = []
        for msg in conversation.messages:
            messages.append({"role": msg.role, "content": msg.content, "created_at": msg.created_at.isoformat()})
        service.cache_conversation(conversation_id, messages)
        return ChatResponse(
            success=True, message="success",
            data={"conversation_id": conversation_id, "title": conversation.title, "messages": messages}
        )
    except Exception as e:
        return ChatResponse(success=False, message=str(e))

@router.put("/conversation/{conversation_id}", response_model=ChatResponse)
async def update_conversation(
    conversation_id: int, body: UpdateTitleRequest,
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        conversation = db.query(DBConversation)\
            .filter(DBConversation.id == conversation_id, DBConversation.user_id == current_user.id).first()
        if not conversation:
            return ChatResponse(success=False, message="对话不存在")
        conversation.title = body.title
        db.commit()
        return ChatResponse(success=True, message="success", data={"title": conversation.title})
    except Exception as e:
        db.rollback()
        return ChatResponse(success=False, message=str(e))

@router.delete("/conversation/{conversation_id}", response_model=ChatResponse)
async def delete_conversation(
    conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        conversation = db.query(DBConversation)\
            .filter(DBConversation.id == conversation_id, DBConversation.user_id == current_user.id).first()
        if not conversation:
            return ChatResponse(success=False, message="对话不存在")
        db.delete(conversation)
        db.commit()
        redis_service.client.delete(f"conversation:{conversation_id}")
        return ChatResponse(success=True, message="success")
    except Exception as e:
        db.rollback()
        return ChatResponse(success=False, message=str(e))
