import jwt
from fastapi import Depends
from sqlalchemy.orm import Session

from core.config import get_db
from database.models import User
from utils.security import (
    oauth2_scheme, 
    SECRET_KEY, 
    ALGORITHM
)
from .exception import (
    InvalidTokenException,
    UserNotFoundException
)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise InvalidTokenException()
    except:
        raise InvalidTokenException()
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise UserNotFoundException()

    return user
