from app.database.models.base import Base
from app.database.models.async_engine import async_engine


async def create_tables() -> None:
    """
    Asynchronously creates all tables defined in the application's metadata.

    Utilizes the async engine to establish a connection and runs a synchronous
    operation to create all tables. In the event of an error during table 
    creation, logs the exception message.

    This function does not return any value.
    """
    async with async_engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print(f'Error creating tables: {e}')