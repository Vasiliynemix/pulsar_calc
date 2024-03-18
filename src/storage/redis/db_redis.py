from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from src.config import Config


class RedisDatabase:
    def __init__(self, cfg: Config) -> None:
        self._cfg = cfg
        self._redis = self.__set_redis()

    async def get_redis(self) -> Redis:
        return self._redis

    def __set_redis(self) -> Redis:
        return Redis(
            db=self._cfg.redis.db,
            host=self._cfg.redis.host,
            password=self._cfg.redis.passwd,
            username=self._cfg.redis.username,
            port=self._cfg.redis.port,
        )

    async def get_redis_storage(self) -> RedisStorage:
        return RedisStorage(
            redis=self._redis,
            state_ttl=self._cfg.redis.state_ttl,
            data_ttl=self._cfg.redis.data_ttl,
        )

    async def set_course_ask(self, course_ask: float) -> None:
        await self._redis.set("course_ask", course_ask)

    async def set_course_btc_ask(self, course_ask: float) -> None:
        await self._redis.set("course_btc_ask", course_ask)

    async def set_course_bid(self, course_bid: float) -> None:
        await self._redis.set("course_bid", course_bid)

    async def get_course_ask(self) -> float | None:
        current_course = await self._redis.get("course_ask")
        return float(current_course) if current_course else None

    async def get_course_btc_ask(self) -> float | None:
        current_course = await self._redis.get("course_btc_ask")
        return float(current_course) if current_course else None

    async def get_course_bid(self) -> float | None:
        current_course = await self._redis.get("course_bid")
        return float(current_course) if current_course else None
