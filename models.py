from enum import unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base
import uuid, secrets
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    token = Column(String, unique = True)
    jobs = relationship("Job", back_populates="owner")

    def __init__(self, email, hashed_password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.hashed_password = self.set_pw(hashed_password)
        self.token = self.set_token(24)
    
    def set_id(self):
        return str(uuid.uuid4())[:8]

    def set_pw(self, password):
        return pwd_context.hash(password)

    def set_token(self, length):
        return secrets.token_hex(length)
    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, index=True)
    url = Column(String, index=True)
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="jobs")