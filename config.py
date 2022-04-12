import os
class Settings:
    PROJECT_NAME: str = 'Job Tracker'
    PROJECT_VERSION: str = '1.0.0'
    SQLALCHEMY_DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URL')

settings = Settings()