import redis
from app.config import settings

redis_client = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password,
    decode_responses=True
)

def get_redis():
    return redis_client