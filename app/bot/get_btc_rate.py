import re

from app.bot.crypto_bot import crypto_bot


def get_btc_rate() -> float:
    """
    Gets the current rate of 1 BTC in RUB from the CryptoPay Bot.

    Returns:
        float: The current rate of 1 BTC in RUB.

    Raises:
        Exception: If there is an error getting the rate.
    """
    try:
        exchange_rates = crypto_bot.get_exchange_rates()

        pattern = re.compile(r'.*BTC.*RUB.*')
        for line in exchange_rates:
            if pattern.match(str(line)):
                btc_to_rubles_line = line
                break
        
        rate = float(re.search(r'rate=(\d*\.\d+|\d+)', str(btc_to_rubles_line)).group(1))

        return rate
    except Exception as e:
        print(f'Error getting BTC rate: {e}')