from typing import List
from uuid import UUID
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from entities.task import Task
from entities.user import User
from models.task import SearchTaskModel, TaskModel, TaskViewModel
from models.user import UserClaims
from services import user as UserService
from services.exception import *
from services.utils import get_current_utc_time


def get_all_tasks(db: Session, conds: SearchTaskModel) -> List[Task]:
    query = select(Task, User).join(User, Task.user_id == User.id)
    
    if conds.user_id is not None:
        query = query.filter(Task.user_id == conds.user_id)
    if conds.status is not None:
        query = query.filter(Task.status == conds.status)
    if conds.priority is not None:
        query = query.filter(Task.priority == conds.priority)
    
    query.offset((conds.page-1)*conds.size).limit(conds.size)

    results = db.execute(query).all()
    tasks = [
        TaskViewModel(
            id=task.id,
            summary=task.summary,
            description=task.description,
            status=task.status,
            priority=task.priority,
            user_id=user.id,
            username=user.username,
            email=user.email,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        for task, user in results
    ]
    
    return tasks


def get_task_by_id(db: Session, id: UUID, with_user = False) -> Task:
    if with_user:
        query = (
            select(Task, User)
            .join(User, Task.user_id == User.id)
            .where(Task.id == id)
        )

        result = db.execute(query).fetchone()
        task, user = result
        return TaskViewModel(
            id=task.id,
            summary=task.summary,
            description=task.description,
            status=task.status,
            priority=task.priority,
            user_id=user.id,
            username=user.username,
            email=user.email,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
    else:
        query = select(Task).filter(Task.id == id)
        return db.scalars(query).first()
    

def add_new_task(db: Session, data: TaskModel, user: UserClaims) -> Task:
    if data.user_id is not None:
        user_info = UserService.get_user_by_id(db, data.user_id, with_company=False)
        if user_info is None:
            raise InvalidInputError("Invalid user information")
    else:
        data.user_id = uuid.UUID(user.sub)

    task = Task(**data.model_dump())
    task.created_at = get_current_utc_time()
    task.updated_at = get_current_utc_time()

    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task

def update_task(db: Session, id: UUID, data: TaskModel, user: UserClaims) -> Task:
    task = get_task_by_id(db, id)

    if task is None:
        raise ResourceNotFoundError()
    
    if not user.is_admin:
        if task.user_id != uuid.UUID(user.sub):
            raise AccessDeniedError
        
    if data.user_id is not None:
        user_info = UserService.get_user_by_id(db, data.user_id, with_company=False)
        if user_info is None:
            raise InvalidInputError("Invalid user information")
    else:
        if user.is_admin:
            data.user_id = uuid.UUID(user.sub)
        else:
            raise AccessDeniedError
    
    task.summary = data.summary
    task.description = data.description
    task.status = data.status
    task.priority = data.priority
    task.user_id = data.user_id
    task.updated_at = get_current_utc_time()
    
    db.commit()
    db.refresh(task)
    
    return get_task_by_id(db, id, with_user=True)
