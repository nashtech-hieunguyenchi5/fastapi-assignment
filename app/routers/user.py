from typing import List
import uuid
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from database import get_db_context
from services import user as UserService
from services.auth import authorizer
from services.exception import *
from models import UserBaseModel, UserViewModel, UserClaims

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserBaseModel])
async def get_users(db: Session = Depends(get_db_context)) -> List[UserBaseModel]:
    return UserService.get_all_user(db)


@router.get("/details", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def get_user_details(db: Session=Depends(get_db_context), user: UserClaims = Depends(authorizer)):
    user_details = UserService.get_user_by_id(db, uuid.UUID(user.sub), with_company=True)

    if user_details is None:
        raise ResourceNotFoundError()

    return user_details