import redis


class RedisService:

    def __init__(self,
                 redis_client: redis.Redis
                 ) -> None:
        self.redis_client = redis_client

    def set_key_value(self, key: str, value: str):
        self.redis_client.setex(key, 5000, value)

    def get_value(self, key: str):
        return self.redis_client.get(key)

    def add_set(self, key: str, value: str) -> int:
        return self.redis_client.sadd(key, value)

    def rem_set(self, key: str, value: str) -> int:
        return self.redis_client.srem(key, value)

    def exists(self, key: str, value: str) -> bool:
        return self.redis_client.sismember(key, value)
