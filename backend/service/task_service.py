from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.websockets import WebSocket

from utils.exception import TaskNotFoundException
from database.models import Task, User
from schema.task_schema import TaskCreate, TaskUpdate


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_status_update(self, task_id: int, status: str):
        for connection in self.active_connections:
            await connection.send_json({"task_id": task_id, "status": status})


websocket_manager = WebSocketManager()

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


async def update_task_service(db: Session, user: User, task_id: int, task_data: TaskUpdate) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
    if not task:
        raise TaskNotFoundException()
    
    old_status = task.status
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    
    if task.status != old_status:
        await websocket_manager.send_status_update(task.id, task.status.value)
    
    return task


def delete_task_service(db: Session, user: User, task_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
    if not task:
        raise TaskNotFoundException()
    
    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted", 
        "detail": None
    }
