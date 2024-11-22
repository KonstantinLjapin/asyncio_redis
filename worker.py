import asyncio
from async_redis import WorkerRedis


async def main():
    redis_worker: WorkerRedis = WorkerRedis(redis_container_name="redis", redis_host_name="localhost", redis_port=6379)
    await redis_worker.connect()

    # Выполнение операций
    await redis_worker.add_capcha_key(1234, 5678)
    value = await redis_worker.get_capcha_key(1234)
    print(f"Captcha key for user 1234: {value}")

    await redis_worker.del_capcha_key(1234)

    # Отключение от Redis
    await redis_worker.disconnect()


# Запуск
asyncio.run(main())

