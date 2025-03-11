import csv
import io

from fastapi.responses import Response
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


def export_task_statistics_to_csv(db: Session):
    stats = get_task_statistics(db)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Метрика", "Значение"])
    writer.writerow(["Всего задач", stats["total_tasks"]])
    for status, count in stats["status_counts"].items():
        writer.writerow([f"Задач со статусом {status}", count])

    avg_time = stats["average_completion_time"]
    writer.writerow(["Среднее время выполнения (сек)", avg_time if avg_time else "N/A"])
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"}
    )
