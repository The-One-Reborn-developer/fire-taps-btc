from app.database.models.base import Base
from app.database.models.async_engine import async_engine


async def create_tables() -> None:
    async with async_engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print(f'Error creating tables: {e}')