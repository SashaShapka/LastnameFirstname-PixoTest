from slowapi import Limiter
from limiter.key_func import get_user_id_key
from settings import settings

limiter = Limiter(key_func=get_user_id_key) if settings.enable_rate_limit else None

def conditional_limiter(limit_value: str):
    def decorator(func):
        if not limiter:
            return func
        return limiter.limit(limit_value)(func)
    return decorator