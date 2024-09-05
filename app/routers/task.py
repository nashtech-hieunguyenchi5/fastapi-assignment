from importlib.metadata import requires
from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session

from database import get_db_context
from services import task as TaskService
from services.exception import *
from models import TaskModel,TaskViewModel, SearchTaskModel, UserClaims
from services.auth import authorizer

router = APIRouter(prefix="/tasks", tags=["Task"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TaskViewModel])
async def get_all_tasks(
    db: Session = Depends(get_db_context),
    user_id: UUID = Query(default=None),
    status: str = Query(default=None),
    priority: str = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    ):
        conds = SearchTaskModel(user_id, status, priority, page, size)
        return TaskService.get_all_tasks(db, conds)


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def get_task_by_id(task_id: UUID, db: Session=Depends(get_db_context)):
    task = TaskService.get_task_by_id(db, task_id, joined_load=True)
    
    if task is None:
        raise ResourceNotFoundError()
    
    return task



@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel, description="Only for Admin")
async def create_task(request: TaskModel, db: Session = Depends(get_db_context),user: UserClaims = Depends(authorizer)):  
    if not user.is_admin:
        raise AccessDeniedError()

    return TaskService.add_new_task(db, request, user)


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_task(
    task_id: UUID,
    request: TaskModel,
    db: Session=Depends(get_db_context),
    user: UserClaims = Depends(authorizer)
    ):
        return TaskService.update_task(db, task_id, request, user)
