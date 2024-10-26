import string
import random


async def registration_referral() -> str:
    """
    Generates a random referral code.

    The referral code is a 10 character string and can contain letters and/or numbers.
    """
    letters = string.ascii_letters + string.digits

    return ''.join(random.choice(letters) for _ in range(10))