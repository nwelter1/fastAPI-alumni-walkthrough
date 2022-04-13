from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class JobBase(BaseModel):
    company: str
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    status: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class User(UserBase):
    id: str
    is_active: bool
    jobs: List[Job] = []
    class Config:
        orm_mode = True

class UserToken(User):
    token: str
