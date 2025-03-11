from sqlalchemy.orm import Session
from typing import List, Optional

from utils.exception import TaskNotFoundException
from database.models import Task, User
from schema.task_schema import TaskCreate, TaskUpdate


def get_tasks_service(db: Session, user: User, status: Optional[str], priority: Optional[str]) -> List[Task]:
    query = db.query(Task).filter(Task.owner_id == user.id)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)

    return query.all()


def create_task_service(db: Session, user: User, task_data: TaskCreate) -> Task:
    new_task = Task(**task_data.dict(), owner_id=user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task_service(db: Session, user: User, task_id: int, task_data: TaskUpdate) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
    if not task:
        raise TaskNotFoundException()

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task_service(db: Session, user: User, task_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
    if not task:
        raise TaskNotFoundException()

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
