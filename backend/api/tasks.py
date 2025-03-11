from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from core.config import get_db
from schema.task_schema import TaskCreate, TaskUpdate, TaskResponse
from service.task_service import (
    get_tasks_service,
    create_task_service,
    update_task_service,
    delete_task_service
)
from utils.dependencies import get_current_user
from database.models import User

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    status: Optional[str] = None, 
    priority: Optional[str] = None, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return get_tasks_service(db=db, user=user, status=status, priority=priority)


@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    return create_task_service(db=db, user=user, task_data=task_data)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, 
    task_data: TaskUpdate, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    return update_task_service(db=db, user=user, task_id=task_id, task_data=task_data)


@router.delete("/{task_id}")
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    return delete_task_service(db=db, user=user, task_id=task_id)
