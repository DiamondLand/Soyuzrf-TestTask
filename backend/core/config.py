from typing import Literal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


MODE: Literal["DEV", "TEST", "STABLE", "PROD"] = "DEV"

APP_TITLE = "TestTask"
APP_DESCRIPTION = "Service for SoyuzRF"
APP_VERSION = "1.0.0"
APPURL = "http://127.0.0.1:9000/"
TG_TOKEN = "7731531116:AAEmm_n-eJfxGKB1xZi82BbmhzWgGXM6yj0"
TG_ID = 872278858

# ======= DataBase Settings ======= #
if MODE == "DEV":
    DATABASE_URL = "sqlite:///database.db"
else:
    DATABASE_URL = "postgres://postgres:postgres@localhost:5432/"

DATABASE_MODULES = {
    "models": [
        "database.models", 
    ]
}
# ======= DataBase Settings ======= #

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
