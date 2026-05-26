from openai import OpenAI
from app.config import settings
from app.models import Conversation, Message
from app.utils.redis import get_redis
from datetime import datetime
import json

class QAService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=f"{settings.deepseek_api_base_url}/v1"
        )
    
    def generate_response(self, messages):
        response = self.client.chat.completions.create(
            model=settings.deepseek_model,
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
            timeout=settings.deepseek_timeout
        )
        return response.choices[0].message.content
    
    def save_conversation(self, db, user_id, messages):
        conversation = Conversation(
            user_id=user_id,
            title=messages[0]["content"][:30] if messages else "新对话"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        for msg in messages:
            message = Message(
                conversation_id=conversation.id,
                role=msg["role"],
                content=msg["content"]
            )
            db.add(message)
        db.commit()
        
        return conversation.id
    
    def get_conversation(self, db, conversation_id):
        return db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    def get_conversations(self, db, user_id, limit=10, offset=0):
        return db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).limit(limit).offset(offset).all()
    
    def update_conversation_title(self, db, conversation_id, title):
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.now()
            db.commit()
        return conversation
    
    def delete_conversation(self, db, conversation_id):
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            db.delete(conversation)
            db.commit()
        return True
    
    def cache_conversation(self, conversation_id, messages):
        redis_client = get_redis()
        key = f"conversation:{conversation_id}"
        redis_client.set(key, json.dumps(messages), ex=3600)
    
    def get_cached_conversation(self, conversation_id):
        redis_client = get_redis()
        key = f"conversation:{conversation_id}"
        data = redis_client.get(key)
        return json.loads(data) if data else None