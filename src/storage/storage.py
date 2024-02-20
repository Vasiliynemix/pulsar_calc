from src.storage.db.connect import DBConnect
from src.storage.redis.db_redis import RedisDatabase


class Storage:
    def __init__(self, db: DBConnect, redis: RedisDatabase) -> None:
        self._db = db
        self._redis = redis

    @property
    def db(self) -> DBConnect:
        return self._db

    @property
    def redis(self) -> RedisDatabase:
        return self._redis
