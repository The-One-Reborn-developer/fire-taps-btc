from sqlalchemy import select

from app.database.models.user import User
from app.database.models.async_session import async_session


async def put_user(telegram_id: int, **kwargs) -> None:
    async with async_session() as session:
        async with session.begin():
            try:
                user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

                if user:
                    for key, value in kwargs.items():
                        setattr(user, key, value)
            except Exception as e:
                print(f'Error updating user: {e}')