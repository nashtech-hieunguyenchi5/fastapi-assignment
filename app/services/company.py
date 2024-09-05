from sqlalchemy import Integer, select
from sqlalchemy.orm import Session
from entities.company import Company
from sqlalchemy.ext.asyncio import AsyncSession


async def get_companies(async_db: AsyncSession) -> list[Company]:
    result = await async_db.scalars(select(Company).order_by(Company.created_at))
    return result.all()


def get_company_by_id(db: Session, company_id: Integer) -> Company:
    return db.scalars(select(Company).filter(Company.id == company_id)).first()