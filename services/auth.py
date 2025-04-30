from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from passlib.hash import bcrypt
from pydantic import ValidationError

from db.db import ProductsDB

from models import models

from apis.schemas.token_model import Token
from apis.schemas.user_input_model import User, UserCreate

from settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/sign-in')

db = ProductsDB()

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.verify_token(token)


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


class AuthService:

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = User.parse_obj({"id": payload.get("sub"), **user_data})
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: models.User) -> Token:
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_s),
            'sub': user.id,
            'user': user.to_dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return Token(access_token=token)


    def register_new_user(
        self,
        user_data: UserCreate,
    ) -> Token:
        with db.session_scope() as session:
            user = models.User(
                username=user_data.username,
                hashed_password=self.hash_password(user_data.password),
                role=user_data.role
            )

            session.add(user)
            session.commit()
        return self.create_token(user)

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )


        with db.session_scope() as session:
            user = session.query(models.User).filter(models.User.username == username).first()

        if not user:
            raise exception

        if not self.verify_password(password, user.hashed_password):
            raise exception

        return self.create_token(user)