import re

from app.bot.crypto_bot import crypto_bot
from app.bot.get_btc_rate import get_btc_rate


async def convert_btc_to_usdt(btc_amount) -> float:
    try:
        exchange_rates = await crypto_bot.get_exchange_rates()

        pattern = re.compile(r'.*USDT.*RUB.*')
        for line in exchange_rates:
            if pattern.match(str(line)):
                usdt_to_rubles_line = line
        
        usdt_rate = float(re.search(r'rate=(\d*\.\d+|\d+)', str(usdt_to_rubles_line)).group(1))
        btc_rate = await get_btc_rate()

        print(f'USDT rate: {usdt_rate}, BTC rate: {btc_rate}')
        return (btc_amount * btc_rate) / usdt_rate
    except Exception as e:
        print(f'Error getting BTC rate: {e}')