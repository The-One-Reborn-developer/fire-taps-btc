from sqlalchemy import select

from app.database.models.user import User
from app.database.models.sync_session import sync_session


def get_user_by_id(telegram_id: int) -> User | None:
    """
    Gets a user by telegram_id from the database.

    Args:
        telegram_id (int): The telegram_id of the user to fetch.

    Returns:
        User | None: The user from the database, or None if no user was found.
    """
    with sync_session() as session:
        with session.begin():
            try:
                user = session.scalar(select(User).where(User.telegram_id == telegram_id))

                if user:
                    return [
                        user.btc_balance,
                        user.referrals_amount,
                        user.registration_referral_code,
                        user.last_played,
                        user.level,
                        user.is_admin,
                        user.number_of_plays,
                        user.play_referral_code
                    ]
                else:
                    return None
            except Exception as e:
                print(f'Error getting user: {e}')