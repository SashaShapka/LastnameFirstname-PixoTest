import json
import functools
import logging

from pydantic.v1.json import pydantic_encoder
from settings import settings
from cache.redis_client import client

logger = logging.getLogger('my_logger')

def cache_response(success_timeout=settings.success_timeout, failure_timeout=settings.failed_timeout):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not settings.use_cache or client is None:
                return await func(*args, **kwargs)

            if func.__name__ == "get_product_by_filters":
                params_words = [str(param) for key, param in kwargs.items() if param is not None and key in ['name',
                                                                                                             'price_min',
                                                                                                             'price_max',
                                                                                                             'price_exact',
                                                                                                             'classification'
                                                                                                             ]
                                ]
                params_suffix = "_".join(params_words)
                cache_key = f"{func.__name__}__static_{params_suffix}"
            else:
                cache_key  = f"{func.__name__}__static_"

            cached = await client.get(cache_key)
            if cached:
                logger.info(" [Redis] Get data from cache")
                return json.loads(cached)

            result = await func(*args, **kwargs)

            try:

                if isinstance(result, list):
                    serializable_result = [r.model_dump() if hasattr(r, "model_dump") else r for r in result]
                else:
                    serializable_result = result.model_dump() if hasattr(result, "model_dump") else result

                await client.set(
                    cache_key,
                    json.dumps(serializable_result, default=pydantic_encoder),
                    ex=success_timeout if result else failure_timeout
                )
                logger.info("[Redis] Set data to the cache")
            except Exception as e:
                logger.error(f"[Redis] Failed set data to cache {e}")
                pass

            return result
        return wrapper
    return decorator
