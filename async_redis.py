from redis import asyncio as aioredis
from typing import List


class WorkerRedis:
    """
    Async Redis worker with a reusable connection.
    """

    def __init__(self, redis_container_name: str, redis_host_name: str, redis_port: int):
        self.__host: str = redis_host_name
        self.__port: int = redis_port
        self.__users_map_name: str = f"{redis_container_name}_users_capcha_key_map"
        self.__users_capcha_flag_map_name: str = f"{redis_container_name}_users_capcha_flag_map"
        self._redis_client = None

    async def connect(self):
        """
        Initializes the Redis connection and stores it as an attribute.
        """
        self._redis_client = await aioredis.from_url("redis://localhost")

    async def disconnect(self):
        """
        Closes the Redis connection if it's open.
        """
        if self._redis_client:
            await self._redis_client.close()
            self._redis_client = None

    async def _ensure_connection(self):
        """
        Ensures the Redis connection is established.
        """
        if not self._redis_client:
            await self.connect()

    async def add_capcha_key(self, user_id: int, capcha: int) -> None:
        await self._ensure_connection()
        await self._redis_client.hset(self.__users_map_name, mapping={str(user_id): capcha})

    async def get_capcha_key(self, user_id: int) -> int:
        await self._ensure_connection()
        value = await self._redis_client.hget(self.__users_map_name, str(user_id))
        return int(value) if value is not None else None

    async def get_all_capcha_user_key(self) -> List[str]:
        await self._ensure_connection()
        return await self._redis_client.hkeys(self.__users_map_name)

    async def del_capcha_key(self, user_id: int) -> None:
        await self._ensure_connection()
        await self._redis_client.hdel(self.__users_map_name, str(user_id))

    async def add_capcha_flag(self, user_id: int, flag: int) -> None:
        await self._ensure_connection()
        await self._redis_client.hset(self.__users_capcha_flag_map_name, mapping={str(user_id): flag})

    async def get_capcha_flag(self, user_id: int) -> int:
        await self._ensure_connection()
        value = await self._redis_client.hget(self.__users_capcha_flag_map_name, str(user_id))
        return int(value) if value is not None else None

    async def change_capcha_flag(self, user_id: int, flag: int) -> None:
        await self.add_capcha_flag(user_id, flag)

    async def del_capcha_flag(self, user_id: int) -> None:
        await self._ensure_connection()
        await self._redis_client.hdel(self.__users_capcha_flag_map_name, str(user_id))

    async def get_all_capcha_users_flag_key(self) -> List[str]:
        await self._ensure_connection()
        return await self._redis_client.hkeys(self.__users_capcha_flag_map_name)

    async def del_all_key(self) -> None:
        await self._ensure_connection()
        user_map_names: List[str] = await self.get_all_capcha_user_key()
        users_capcha_flag: List[str] = await self.get_all_capcha_users_flag_key()
        for key in user_map_names:
            await self.del_capcha_key(int(key))
        for key in users_capcha_flag:
            await self.del_capcha_flag(int(key))
