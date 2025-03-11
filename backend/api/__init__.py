from fastapi import APIRouter
from api import (
    auth, tasks,
    analytics
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
api_router.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])
api_router.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
