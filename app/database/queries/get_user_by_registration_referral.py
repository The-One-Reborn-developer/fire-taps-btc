from sqlalchemy import select

from app.database.models.user import User
from app.database.models.sync_session import sync_session

from app.database.queries.put_user import put_user


def get_user_by_registration_referral(referral_code: str) -> bool:
    """
    Checks if the user's registration referral code matches the current registration referral.

    Args:
        referral_code (str): The referral code to check.

    Returns:
        bool: True if the user's registration referral code matches the current registration referral, False otherwise.
    """
    with sync_session() as session:
        with session.begin():
            try:
                with open('app/temp/universal_registration_referral.txt', 'r') as f:
                    universal_registration_referral = f.read()

                if referral_code == universal_registration_referral:
                    return True

                user = session.scalar(select(User).where(User.registration_referral_code == referral_code))

                if user:
                    put_user(user.telegram_id, referrals_amount=user.referrals_amount + 1)
                    
                    return True
                else:
                    return False
            except Exception as e:
                print(f'Error getting user: {e}')