from fastapi import FastAPI
from tortoise import Tortoise

from utils.redis import RedisUtil
from my_logger import logger
from core import config


async def init_database():
    await RedisUtil.init_redis()
    logger.info("Redis started")
    logger.info("Initializing database")
    await Tortoise.init(
        db_url=config.DATABASE_URL,
        modules=config.DATABASE_MODULES
    )
    await Tortoise.generate_schemas()


async def lifespan(app: FastAPI):
    logger.info("Server started")
    await init_database()
    yield
    logger.info("Server stopped")
