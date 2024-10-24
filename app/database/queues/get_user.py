from sqlalchemy import select

from app.database.models.user import User
from app.database.models.async_session import async_session


async def get_user(telegram_id: int) -> User | None:
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if user:
                return [
                    user.phone,
                ]
            
            return None