from pydantic import BaseModel
from uuid import UUID
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    id: UUID
    username: str
    hashed_password: str
    role: UserRole


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.user