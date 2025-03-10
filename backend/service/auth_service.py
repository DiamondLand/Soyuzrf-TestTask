from sqlalchemy.orm import Session

from database.models import User
from schema.auth_schema import UserCreate
from utils.security import (
    get_password_hash, 
    create_access_token, 
    verify_password
)
from utils.exception import EmailRegisteredException, CredentialsException


def create_user(user_data: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise EmailRegisteredException()

    hashed_password = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(
        data={"sub": new_user.email}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "detail": None
    }


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def login_user(user_data, db: Session):
    user = db.query(User).filter(User.email == user_data.username).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise CredentialsException

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
