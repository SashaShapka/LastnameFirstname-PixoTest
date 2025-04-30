from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, String, Float, Integer, DateTime, Index, Enum as PgEnum
from models.allocator import UUID_F
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from apis.schemas.user_input_model import UserRole

Base = declarative_base()

class ProductClassification(str, Enum):
    education = "education"
    gaming = "gaming"
    home_goods = "home_goods"

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID_F(), default=UUID_F.uuid_allocator, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Integer, nullable=False, default=0)
    classification = Column(String(500), nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID_F(), default=UUID_F.uuid_allocator, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(PgEnum(UserRole, name="user_role"), nullable=False, default=UserRole.user)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __init__(self,username, hashed_password, role):
        self.username = username
        self.hashed_password = hashed_password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "hashed_password": self.hashed_password,
            "role":self.role
        }

class UserProductRequest(Base):
    __tablename__ = "user_product_requests"

    id = Column(UUID_F(), default=UUID_F.uuid_allocator, primary_key=True)
    user_id = Column(UUID_F(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(UUID_F(), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    requested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product"),
        Index("ix_user_product", "user_id", "product_id"),
    )

    user = relationship("User", backref="requested_products")
    product = relationship("Product", backref="requesting_users")



