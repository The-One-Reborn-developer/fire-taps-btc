import re

from app.bot.crypto_bot import crypto_bot


async def get_balance() -> float:
    try:
        balance_data = await crypto_bot.get_balance()
        
        pattern = re.compile(r'.*BTC.*')
        for line in balance_data:
            if pattern.match(str(line)):
                btc_balance_line = str(line)
        
        btc_balance_line_split = btc_balance_line.split()

        btc_balance = float(btc_balance_line_split[1].split('=')[1])

        return btc_balance
    except Exception as e:
        print(f'Error getting balance: {e}')