from cryptopay.types import Check

from app.bot.crypto_bot import crypto_bot


async def create_check(amount) -> Check | int:
    """
    Creates a check for the specified amount in USDT using the crypto bot.

    :param amount: The amount for which to create the check.
    :return: A Check object if successful, or 400 if there is a validation error with the input amount.
    """
    try:
        check = await crypto_bot.create_check(float(amount), 'USDT')

        return check
    except Exception as e:
        print(f'Create check error: {e}')

        error_code = int(str(e).split(' ')[0].strip('[]'))
        if error_code == 400:
            return 400