from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str

class UserBaseModel(BaseModel):
    id: UUID
    username: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True
    
class UserViewModel(UserBaseModel):
    email: str
    company_id: int
    company_name: str | None = None
    is_admin: bool
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

class UserClaims(BaseModel):
    sub: str
    username: str = None
    email: str = None
    first_name: str
    last_name: str
    is_active: bool = False
    is_admin: bool = False
    aud: str = None
    iss: str = None
    iat: int
    exp: int
