from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from database.models import Task


def get_task_statistics(db: Session):
    total_tasks = db.query(Task).count()

    # Количество задач по статусам
    task_status_counts = (
        db.query(Task.status, func.count())
        .group_by(Task.status)
        .all()
    )
    status_counts = {status: count for status, count in task_status_counts}

    # Среднее время выполнения (для завершенных задач)
    avg_completion_time = (
        db.query(func.avg(Task.deadline - Task.created_at))
        .filter( Task.status == "completed")
        .scalar()
    )

    return {
        "total_tasks": total_tasks,
        "status_counts": status_counts,
        "average_completion_time": avg_completion_time.total_seconds() if avg_completion_time else None,
        "detail": None
    }
