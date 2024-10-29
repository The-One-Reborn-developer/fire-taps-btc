from sqlalchemy import select

from app.database.models.user import User
from app.database.models.sync_session import sync_session


def get_user_by_play_referral(telegram_id: int) -> bool:
    """
    Checks if the user's play referral code matches the current play referral.

    Args:
        telegram_id (int): The telegram ID of the user to check.

    Returns:
        bool: True if the user's play referral code matches the current play referral, False otherwise.
    """
    with sync_session() as session:
        with session.begin():
            try:
                with open('app/temp/play_referral_code.txt', 'r') as f:
                    play_referral = f.read()

                user = session.scalar(select(User).where(User.telegram_id == telegram_id))

                if user:
                    if user.play_referral_code == play_referral:
                        return True
                    else:
                        return False
                else:
                    return False
            except Exception as e:
                print(f'Error getting user: {e}')