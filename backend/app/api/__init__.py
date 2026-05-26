from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import QAService
from app.utils.database import get_db
from app.utils.redis import get_redis
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/qa", tags=["AI问答"])

class MessageItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[MessageItem]
    conversation_id: Optional[int] = None
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        service = QAService()
        
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        
        response_content = service.generate_response(messages)
        
        messages.append({"role": "assistant", "content": response_content})
        
        if request.conversation_id:
            service.cache_conversation(request.conversation_id, messages)
        else:
            conversation_id = service.save_conversation(db, request.user_id, messages)
            service.cache_conversation(conversation_id, messages)
            request.conversation_id = conversation_id
        
        return ChatResponse(
            success=True,
            message="success",
            data={
                "conversation_id": request.conversation_id,
                "response": response_content,
                "messages": messages
            }
        )
    except Exception as e:
        return ChatResponse(
            success=False,
            message=str(e)
        )

@router.get("/conversations", response_model=ChatResponse)
async def get_conversations(user_id: str = "default_user", limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    try:
        service = QAService()
        conversations = service.get_conversations(db, user_id, limit, offset)
        
        result = []
        for conv in conversations:
            result.append({
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            })
        
        return ChatResponse(
            success=True,
            message="success",
            data={"conversations": result}
        )
    except Exception as e:
        return ChatResponse(
            success=False,
            message=str(e)
        )

@router.get("/conversation/{conversation_id}", response_model=ChatResponse)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    try:
        service = QAService()
        
        cached = service.get_cached_conversation(conversation_id)
        if cached:
            return ChatResponse(
                success=True,
                message="success",
                data={"messages": cached}
            )
        
        conversation = service.get_conversation(db, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="对话不存在")
        
        messages = []
        for msg in conversation.messages:
            messages.append({
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            })
        
        service.cache_conversation(conversation_id, messages)
        
        return ChatResponse(
            success=True,
            message="success",
            data={
                "conversation_id": conversation_id,
                "title": conversation.title,
                "messages": messages
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ChatResponse(
            success=False,
            message=str(e)
        )

class UpdateTitleRequest(BaseModel):
    title: str


@router.put("/conversation/{conversation_id}", response_model=ChatResponse)
async def update_conversation(conversation_id: int, body: UpdateTitleRequest, db: Session = Depends(get_db)):
    try:
        service = QAService()
        conversation = service.update_conversation_title(db, conversation_id, body.title)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="对话不存在")
        
        return ChatResponse(
            success=True,
            message="success",
            data={"title": conversation.title}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        return ChatResponse(
            success=False,
            message=str(e)
        )

@router.delete("/conversation/{conversation_id}", response_model=ChatResponse)
async def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    try:
        service = QAService()
        service.delete_conversation(db, conversation_id)
        
        redis_client = get_redis()
        redis_client.delete(f"conversation:{conversation_id}")
        
        return ChatResponse(
            success=True,
            message="success"
        )
    except Exception as e:
        return ChatResponse(
            success=False,
            message=str(e)
        )