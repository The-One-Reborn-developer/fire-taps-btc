import re

from app.bot.crypto_bot import crypto_bot


async def get_balance() -> float:
    try:
        balance_data = await crypto_bot.get_balance()
        
        pattern = re.compile(r'.*USDT.*')
        for line in balance_data:
            if pattern.match(str(line)):
                usdt_balance_line = str(line)
        
        usdt_balance_line_split = usdt_balance_line.split()

        usdt_balance = float(usdt_balance_line_split[1].split('=')[1])

        return usdt_balance
    except Exception as e:
        print(f'Error getting balance: {e}')