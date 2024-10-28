from cryptopay.types import Check

from app.bot.crypto_bot import crypto_bot


async def create_check(amount) -> Check | int:
    try:
        check = await crypto_bot.create_check(float(amount), 'BTC')

        return check
    except Exception as e:
        print(f'Create check error: {e}')

        error_code = int(str(e).split(' ')[0].strip('[]'))
        if error_code == 400:
            return 400