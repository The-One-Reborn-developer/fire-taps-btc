from sqlalchemy import select

from app.database.models.user import User
from app.database.models.async_session import async_session


async def get_user_by_play_referral(telegram_id: int) -> bool:
    async with async_session() as session:
        async with session.begin():
            try:
                with open('app/temp/play_referral_code.txt', 'r') as f:
                    play_referral = f.read()

                user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

                if user:
                    if user.play_referral_code == play_referral:
                        return True
                    else:
                        return False
                else:
                    return False
            except Exception as e:
                print(f'Error getting user: {e}')