import aioredis


class RedisUtil:
    redis = None

    @classmethod
    async def init_redis(cls):
        redis_url = "redis://localhost:6379/0"
        cls.redis = aioredis.from_url(redis_url)
