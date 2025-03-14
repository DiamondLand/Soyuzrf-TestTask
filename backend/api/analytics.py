from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.config import get_db
from service.analytics_service import get_task_statistics, export_task_statistics_to_csv
from utils.dependencies import get_current_user
from database.models import User

router = APIRouter()


@router.get("/task-stats")
def task_statistics(
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    return get_task_statistics(db=db)


@router.get("/csv")
def export_csv(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return export_task_statistics_to_csv(db)
