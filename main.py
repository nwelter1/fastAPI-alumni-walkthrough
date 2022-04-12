from datetime import datetime
from fastapi import FastAPI, Request, APIRouter
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import settings
from pydantic import BaseModel
from datetime import datetime as date


class Job(BaseModel):
    company: str
    title: str
    status: str
    description: Optional[str] = None
    date_applied: Optional[datetime] = date.now()
    
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.mount('/static', StaticFiles(directory='static'), name = 'static')
templates = Jinja2Templates(directory = 'templates')

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('pages/home.html', {'request': request})

@app.post('/jobs/')
async def create_job(job: Job):
    return job