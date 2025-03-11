from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.config import get_db
from schema.auth_schema import UserCreate, Token
from service.auth_service import create_user, login_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", response_model=Token)
def register(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    return create_user(user_data=user_data, db=db)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    return login_user(user_data=form_data, db=db)
