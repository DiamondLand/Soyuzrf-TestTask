from pydantic import BaseModel, Field, validator
from datetime import datetime, timezone
from typing import Optional

from database.models import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str]
    deadline: datetime
    priority: TaskPriority = TaskPriority.medium

    @validator("deadline")
    def validate_deadline(cls, value):
        if value is not None:
            if value.tzinfo is not None:
                value = value.astimezone(timezone.utc).replace(tzinfo=None)  # Приводим к UTC без таймзоны
            
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            if value < today:
                raise ValueError("Deadline cannot be before today")
        
        return value

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    deadline: Optional[datetime]
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]

    @validator("deadline")
    def validate_deadline(cls, value):
        if value is not None:
            if value.tzinfo is not None:
                value = value.astimezone(timezone.utc).replace(tzinfo=None)  # Приводим к UTC без таймзоны
            
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            if value < today:
                raise ValueError("Deadline cannot be before today")
        
        return value

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
