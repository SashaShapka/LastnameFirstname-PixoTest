from fastapi import Request
from slowapi.util import get_remote_address

limiter = None

def get_user_id_key(request: Request):
    try:
        user = request.state.user
        return str(user.id) if user else get_remote_address(request)
    except Exception:
        return get_remote_address(request)