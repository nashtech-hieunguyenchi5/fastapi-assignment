from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class CompanyModel(BaseModel):
    name: str
    description: str
    mode: str
    rating: str

class CompanyBaseModel(BaseModel):
    id: int
    name: str
    description: str
    mode: str | None = None
    rating: str | None = None

    class Config:
        from_attributes = True
    
class CompanyViewModel(CompanyBaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
