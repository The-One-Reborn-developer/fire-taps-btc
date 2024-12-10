from aiocpa.types import Check

from app.bot.crypto_bot import crypto_bot


def create_check(amount) -> Check | int:
    """
    Creates a check for the specified amount in USDT using the crypto bot.
    
    Args:
        amount: The amount for which to create the check.
    Returns:
        Check | int: A Check object if successful, or 400 if there is a validation error with the input amount.
    """
    try:
        check = crypto_bot.create_check(float(amount), 'USDT')

        return check
    except Exception as e:
        print(f'Create check error: {e}')

        error_code = int(str(e).split(' ')[0].strip('[]'))
        if error_code == 400:
            return 400