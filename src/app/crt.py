import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

import sys

sys.path.append('src')

from app.multipart.models import Base
from app.env import DATABASE_URL


async def async_main() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(async_main())
