from typing import Optional
from functools import wraps
from fastapi import Request, Header, HTTPException

# potentially just add this functionality into the route itself...
# not as clean but the only way it will work for auto generated docs...
def verify_token(x_access_token: str = Header(...)):
    if x_access_token != 'Test':
        raise HTTPException(status_code=400, detail="X-Token header invalid")


