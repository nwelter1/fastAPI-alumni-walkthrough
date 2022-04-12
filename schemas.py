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

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    is_active: bool
    jobs: List[Job] = []
    class Config:
        orm_mode = True