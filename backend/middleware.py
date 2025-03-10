import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from my_logger import logger


class TimeMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()
        response = await call_next(request)
        execute_time = str(round((time.time() - start_time), 4))
        response.headers["X-execute-time"] = execute_time
        if not "actor" in request.url.path:
            print(f"From {request.url.path} by {execute_time} seconds")
            logger.info(
                f"[ET] Request: {request.url.path}, Execution Time: {execute_time} seconds",
                extra={
                    "path": request.url.path,
                    "execution_time": round((time.time() - start_time), 4),
                    "method": request.method,
                    "remote_addr": request.client.host,
                    "user_agent": request.headers.get("User-Agent") or "",
                },
            )
        return response
