import string
import random


async def registration_referral() -> str:
    """
    Generates a random referral code.

    The referral code is a 10 character string and can contain letters and/or numbers.

    Returns:
        str: The generated referral code.
    """
    try:
        letters = string.ascii_letters + string.digits

        return ''.join(random.choice(letters) for _ in range(10))
    except Exception as e:
        print(f'Error generating registration referral: {e}')
