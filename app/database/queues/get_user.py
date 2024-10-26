from sqlalchemy import select

from app.database.models.user import User
from app.database.models.async_session import async_session


async def get_user(telegram_id: int) -> User | None:
    async with async_session() as session:
        async with session.begin():
            try:
                user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

                if user:
                    return [
                        user.phone,
                        user.btc_balance,
                        user.referrals_amount,
                        user.referral_code
                    ]
                else:
                    return None
            except Exception as e:
                print(f'Error getting user: {e}')