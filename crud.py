from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_email_pw(db: Session, email: str, password: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_jobs(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.id == user_id).first().jobs


def create_user_job(db: Session, job: schemas.JobCreate, user_id: str):
    db_job = models.Job(**job.dict(), owner_id=user_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job