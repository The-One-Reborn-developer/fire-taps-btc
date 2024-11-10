import string
import random


async def play_referral() -> None:
    """
    Generates a random referral code for a play.

    The referral code is a 15 character string and can contain letters and/or numbers.

    Returns:
        None
    """
    try:
        letters = string.ascii_letters + string.digits

        code = ''.join(random.choice(letters) for _ in range(15))

        with open('app/temp/play_referral_code.txt', 'w') as f:
            f.write(code)
    except Exception as e:
        print(f'Error generating play referral: {e}')
