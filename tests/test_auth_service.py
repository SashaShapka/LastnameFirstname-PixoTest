import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from jose import jwt
from passlib.hash import bcrypt
from fastapi import HTTPException, status

from apis.schemas.user_input_model import UserRole
from settings import settings
from services.auth import AuthService


class MockUser:
    def __init__(self, username, password, role=UserRole.user):
        self.id = str(uuid4())
        self.username = username
        self.hashed_password = bcrypt.hash(password)
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "hashed_password": self.hashed_password,
            "role": self.role
        }


def test_hash_and_verify_password():
    raw_password = "secret123"
    hashed = AuthService.hash_password(raw_password)
    assert bcrypt.verify(raw_password, hashed)
    assert AuthService.verify_password(raw_password, hashed)


def test_create_token_and_verify_jwt_content():
    user = MockUser(username="testuser", password="secret", role=UserRole.admin)
    token = AuthService.create_token(user)
    decoded = jwt.decode(token.access_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    assert decoded["sub"] == user.id
    assert decoded["user"]["username"] == user.username
    assert decoded["user"]["role"] == user.role


def test_verify_token_valid():
    user = MockUser(username="validuser", password="pass")
    token = AuthService.create_token(user)
    verified_user = AuthService.verify_token(token.access_token)
    assert verified_user.username == user.username
    assert verified_user.role == user.role


def test_verify_token_invalid_signature():
    fake_token = jwt.encode(
        {
            "sub": str(uuid4()),
            "user": {"username": "x", "hashed_password": "y", "role": "user"},
            "exp": datetime.utcnow() + timedelta(seconds=60)
        },
        "wrong_secret",
        algorithm=settings.jwt_algorithm
    )
    with pytest.raises(HTTPException) as exc:
        AuthService.verify_token(fake_token)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
