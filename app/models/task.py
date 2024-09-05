from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from entities.task import TaskStatus, TaskPriority



class SearchTaskModel():
    def __init__(self, user_id, status, priority, page, size) -> None:
        self.user_id = user_id
        self.status = status
        self.priority = priority
        self.page = page
        self.size = size

class TaskModel(BaseModel):
    summary: str = Field(min_length=2)
    description: str = Field(min_length=2)
    status: TaskStatus = Field(default=TaskStatus.OPEN)
    priority: TaskPriority = Field(default=TaskPriority.NORMAL)
    user_id: UUID | None = None


class TaskViewModel(BaseModel):
    id: UUID 
    summary: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    user_id: UUID
    username: str | None = None
    email: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True
