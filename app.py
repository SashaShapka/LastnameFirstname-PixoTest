from fastapi import FastAPI
from cache.redis_client import init_redis_client
from db.db_utils import init_db
from limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from logging_conf import setup_logging


setup_logging()
init_db()
init_redis_client()

tags_metadata = [
    {
        'name': 'LastnameFirstname-PixoTest',
        'description': 'Products Manager',
    },
]

app = FastAPI(
    version='1.0.0',
    openapi_tags=tags_metadata,
)

if limiter:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from routers import register_routes
register_routes(app)

