from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from database.models import Task, User


def get_task_statistics(db: Session, user: User):
    total_tasks = db.query(Task).filter(Task.owner_id == user.id).count()
    completed_tasks = db.query(Task).filter(Task.owner_id == user.id, Task.status == "completed").count()
    pending_tasks = total_tasks - completed_tasks
    avg_priority = db.query(func.avg(Task.priority)).filter(Task.owner_id == user.id).scalar()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "average_priority": avg_priority,
        "detail": None
    }
