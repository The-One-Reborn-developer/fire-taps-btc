import re

from app.bot.crypto_bot import crypto_bot
from app.bot.get_btc_rate import get_btc_rate


def convert_btc_to_usdt(btc_amount: float) -> float | None:
    """
    Converts the given amount of Bitcoin to USDT.

    :param btc_amount: The amount of Bitcoin to convert.
    :return: The converted amount of USDT or 0.0 if conversion fails.
    """
    try:
        exchange_rates = crypto_bot.get_exchange_rates()

        # Check if exchange rates are retrieved successfully
        if not exchange_rates:
            print('Error: No exchange rates retrieved.')
            return None

        pattern = re.compile(r'.*USDT.*RUB.*')
        usdt_to_rubles_line = None
        
        # Find the relevant line for USDT to RUB
        for line in exchange_rates:
            if pattern.match(str(line)):
                usdt_to_rubles_line = line
                break  # Break after finding the first match
        
        if usdt_to_rubles_line is None:
            print('Error: USDT to RUB line not found in exchange rates.')
            return None

        usdt_rate = float(re.search(r'rate=(\d*\.\d+|\d+)', str(usdt_to_rubles_line)).group(1))

        btc_rate = get_btc_rate()
        
        if btc_rate is None:  # Check if btc_rate is None
            print('Error: BTC rate is None.')
            return None

        usdt_amount = (btc_amount * btc_rate) / usdt_rate
        print(f'Converted {btc_amount} BTC to {usdt_amount} USDT.')
        
        return usdt_amount
    except Exception as e:
        print(f'Error getting BTC rate: {e}')