from app.database.models.base import Base
from app.database.models.async_engine import async_engine


async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)