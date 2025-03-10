import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from core import config
from core.lifespan import lifespan
from api import api_router
from core.config import Base, engine
from middleware import TimeMiddleware

start_time = time.time()
app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.get("/uptime")
def uptime():
    return {"uptime": time.time() - start_time}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TimeMiddleware)
app.include_router(api_router)
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    run(app, port=9000)
