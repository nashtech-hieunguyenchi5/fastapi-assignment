from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Uuid
from database import Base
from entities.base_entity import BaseEntity
from passlib.context import CryptContext
from sqlalchemy.orm import relationship
import uuid

bcrypt_context = CryptContext(schemes=["bcrypt"])

class User(BaseEntity, Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="user")

    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="users")


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)
