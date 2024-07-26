import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

import sys

sys.path.append('src')

from app.multipart.models.user import User
from app.multipart.models.task import Task
from app.env import DATABASE_URL


async def async_main() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Task.metadata.drop_all)
        await conn.run_sync(Task.metadata.create_all)


asyncio.run(async_main())  # Очистка и добавление таблиц в Postgres
