from settings import settings
import redis.asyncio as redis
import logging

logger = logging.getLogger("my_logger")
client = None

def init_redis_client():
    global client
    client = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
    )

    try:
        client.ping()
        logger.info("[Redis] is avaliable")
    except redis.ConnectionError as e:
        logger.error(f"[Redis] Error ping {e}")
