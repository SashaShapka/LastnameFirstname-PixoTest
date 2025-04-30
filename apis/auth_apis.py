from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from services.auth import AuthService, get_current_user
from apis.schemas.user_input_model import UserCreate, User


def sign_up(
    user_data: UserCreate,
    auth_service: AuthService = Depends(),
):
    return auth_service.register_new_user(user_data)

def sign_in(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    return auth_service.authenticate_user(
        auth_data.username,
        auth_data.password,
    )

def get_user(user: User = Depends(get_current_user)):
    return user