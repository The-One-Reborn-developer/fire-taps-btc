import re

from app.bot.create_instance import crypto_bot


async def get_btc_rate() -> float:
    try:
        exchange_rates = await crypto_bot.get_exchange_rates()

        pattern = re.compile(r'.*BTC.*RUB.*')
        for line in exchange_rates:
            if pattern.match(str(line)):
                btc_to_rubles_line = line
        
        rate = float(re.search(r'rate=(\d*\.\d+|\d+)', str(btc_to_rubles_line)).group(1))

        return rate
    except Exception as e:
        print(f'Error getting BTC rate: {e}')