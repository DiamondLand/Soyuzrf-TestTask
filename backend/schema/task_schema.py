from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from database.models import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str]
    deadline: datetime
    priority: TaskPriority = TaskPriority.medium


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    deadline: Optional[datetime]
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    deadline: datetime
    status: TaskStatus
    priority: TaskPriority
    owner_id: int

    class Config:
        from_attributes = True
