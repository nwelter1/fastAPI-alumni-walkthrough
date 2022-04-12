from typing import Optional
from functools import wraps
from fastapi import Request, Header, HTTPException

def verify_token(x_access_token: str = Header(...)):
    if x_access_token != 'Test':
        raise HTTPException(status_code=400, detail="X-Token header invalid")


