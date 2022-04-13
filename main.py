from datetime import datetime
from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException, Header
from typing import Optional, List
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import settings
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from helpers import verify_token
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


models.Base.metadata.create_all(bind=engine)


    
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.mount('/static', StaticFiles(directory='static'), name = 'static')
templates = Jinja2Templates(directory = 'templates')

# Deps
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('pages/home.html', {'request': request})


# Creating a User
@app.post('/users/', response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Getting all users
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Getting one Specific user
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Getting all jobs for one user
@app.post("/users/{user_id}/jobs/", response_model=schemas.Job)
def create_job_for_user(
    user_id: int, job: schemas.JobCreate, db: Session = Depends(get_db)
):
    return crud.create_user_job(db=db, job=job, user_id=user_id)



# User Auth/Login to gain access to token
@app.get('/users/{user_id}/{password}', response_model=schemas.UserToken)
def get_token(user_id: str, password: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not db_user.verify_password(password):
        raise HTTPException(status_code=404, detail="Invalid Password for User")
    else:
        return db_user

# Get all jobs for a specified user
@app.get("/jobs/{user_id}", response_model=List[schemas.Job])
def read_jobs(user_id: str, x_access_token: str = Header(...), skip: int = 0,  limit: int = 100, db: Session = Depends(get_db)):
    token = x_access_token.split(' ')[1]
    db_user = crud.get_user(db, user_id=user_id)
    if token != db_user.token:
        return HTTPException(status_code=401, detail="token does not match for this user")
    jobs = crud.get_jobs(db, user_id=user_id, skip=skip, limit=limit)
    return jobs