import os
from pydantic import BaseSettings
class Settings(BaseSettings):
    PROJECT_NAME: str = 'Job Tracker'
    PROJECT_VERSION: str = '1.0.0'
    SQLALCHEMY_DATABASE_URL: str = os.environ.get('SQLALCHEMY_DATABASE_URL')
    class Config:
        env_file = ".env"

settings = Settings()