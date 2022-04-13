from typing import Optional
from functools import wraps
from fastapi import Request, Header, HTTPException
from sqlalchemy.orm import Session
import crud

import models, schemas
# potentially just add this functionality into the route itself...
# not as clean but the only way it will work for auto generated docs...
def verify_token(db: Session, token: str, user_id: str):
    token = token.split(' ')[1]
    db_user = crud.get_user(db, user_id=user_id)
    print(db_user.token, token)
    if token == db_user.token:
        return True
    elif not db_user:
        raise HTTPException(status_code=404, detail="User Not found")
    elif not token == db_user.token:
        raise HTTPException(status_code=401, detail="Token does not match for this user")
    else:
        return False
    



