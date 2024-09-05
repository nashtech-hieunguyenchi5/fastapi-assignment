from pydantic import BaseModel

class TaskBase(BaseModel):
    summary: str
    description: str
    status: str
    priority: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    tasks: list[Task] = []

    class Config:
        orm_mode = True

class CompanyBase(BaseModel):
    name: str
    description: str
    mode: str
    rating: int

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    employees: list[User] = []

    class Config:
        orm_mode = True
