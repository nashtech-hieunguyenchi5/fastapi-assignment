from typing import List
from uuid import UUID
from sqlalchemy import Integer, select
from sqlalchemy.orm import Session, joinedload
from entities.company import Company
from sqlalchemy.ext.asyncio import AsyncSession


async def get_companies(async_db: AsyncSession) -> list[Company]:
    result = await async_db.scalars(select(Company).order_by(Company.created_at))
    return result.all()


def get_company_by_id(db: Session, company_id: Integer) -> Company:
    return db.scalars(select(Company).filter(Company.id == company_id)).first()
    

# def add_new_book(db: Session, data: BookModel) -> Book:
#     author = AuthorService.get_author_by_id(db, data.author_id)
        
#     if author is None:
#         raise InvalidInputError("Invalid author information")

#     book = Book(**data.model_dump())
#     book.created_at = get_current_utc_time()
#     book.updated_at = get_current_utc_time()

#     db.add(book)
#     db.commit()
#     db.refresh(book)
    
#     return book

# def update_book(db: Session, id: UUID, data: BookModel) -> Book:
#     book = get_book_by_id(db, id)

#     if book is None:
#         raise ResourceNotFoundError()

#     if data.author_id != book.author_id:
#         author = AuthorService.get_author_by_id(db, data.author_id)
#         if author is None:
#             raise InvalidInputError("Invalid author information")
    
#     book.title = data.title
#     book.description = data.description
#     book.mode = data.mode
#     book.rating = data.rating
#     book.updated_at = get_current_utc_time()
    
#     db.commit()
#     db.refresh(book)
    
#     return book
