import asyncio
from app import engine, Base
from app import Task


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы созданы")


asyncio.run(init_db())
