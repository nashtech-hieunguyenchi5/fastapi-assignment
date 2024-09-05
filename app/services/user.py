from typing import Optional, List
from datetime import timedelta
from uuid import UUID
import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models.user import UserClaims, UserViewModel
from entities.user import User, verify_password
from entities.company import Company
from services.utils import get_current_timestamp
from settings import JWT_ALGORITHM, JWT_SECRET


def create_access_token(user: User, expires: Optional[int] = None):
    claims = UserClaims(
        sub=str(user.id),
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_admin=user.is_admin,
        aud='FastAPI',
        iss='FastAPI',
        iat=get_current_timestamp(),
        exp=get_current_timestamp() + expires if expires else get_current_timestamp() + int(timedelta(minutes=10).total_seconds())
    )
    return jwt.encode(claims.model_dump(), JWT_SECRET, algorithm=JWT_ALGORITHM)

def authenticate_user(username: str, password: str, db: Session):
    user = db.scalars(select(User).filter(User.username == username, User.is_active == True)).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



def get_all_user(db: Session, joined_load = False) -> List[User]:
    query = select(User).filter(User.is_active == True)

    if joined_load:
        query.options(joinedload(User.company, innerjoin=True))

    return db.scalars(query).all()


def get_user_by_id(db: Session, id: UUID, with_company: bool = False) -> User:
    if with_company:
        query = (
            select(User, Company)
            .join(Company, User.company_id == Company.id)
            .where(User.id == id, User.is_active == True)
        )

        result = db.execute(query).fetchone()
        user, company = result
        return UserViewModel(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            company_id=user.company_id,
            company_name=company.name,
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    else:
        query = select(User).where(User.id == id, User.is_active == True)
        return db.scalars(query).first()