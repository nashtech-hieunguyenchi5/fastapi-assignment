import enum
from sqlalchemy import Column, Uuid, String, ForeignKey, Enum
from entities.base_entity import BaseEntity
from sqlalchemy.orm import relationship
from database import Base
import uuid

class TaskStatus(enum.Enum):
    OPEN = 'OPEN'
    PROCESSING = 'PROCESSING'
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'

class TaskPriority(enum.Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3

class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    summary = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.OPEN)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.NORMAL)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="tasks")