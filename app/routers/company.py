from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db_context, get_db_context
from models.company import CompanyModel, CompanyViewModel
from services.exception import ResourceNotFoundError
from services import company as CompanyService
from typing import List

router = APIRouter(prefix="/company", tags=["Company"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[CompanyViewModel])
async def get_all_company(async_db: AsyncSession = Depends(get_async_db_context)):
    return await CompanyService.get_companies(async_db)


@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def get_company_by_id(company_id: int, db: Session = Depends(get_db_context)):    
    company = CompanyService.get_company_by_id(db, company_id)

    if company is None:
        raise ResourceNotFoundError()

    return company


# @router.post("", status_code=status.HTTP_201_CREATED, response_model=AuthorViewModel)
# async def create_author(request: AuthorModel, db: Session = Depends(get_db_context)):
#     return AuthorService.add_new_author(db, request)


# @router.put("/{author_id}", status_code=status.HTTP_200_OK, response_model=AuthorViewModel)
# async def update_author(
#     author_id: UUID,
#     request: AuthorModel,
#     db: Session = Depends(get_db_context),
#     ):
#         return AuthorService.update_author(db, author_id, request)


# @router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_author(author_id: UUID, db: Session = Depends(get_db_context)):
#     AuthorService.delete_author(db, author_id)
