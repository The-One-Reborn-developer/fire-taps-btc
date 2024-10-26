import os
import re

from cryptopay import CryptoPay, TESTNET

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


async def get_btc_rate():
    try:
        crypto_bot = CryptoPay(os.getenv('CRYPTO_BOT_TOKEN'), api_server=TESTNET)

        exchange_rates = await crypto_bot.get_exchange_rates()

        pattern = re.compile(r'.*BTC.*RUB.*')
        for line in exchange_rates:
            if pattern.match(str(line)):
                btc_to_rubles_line = line
        
        rate = float(re.search(r'rate=(\d*\.\d+|\d+)', str(btc_to_rubles_line)).group(1))

        return rate
    except Exception as e:
        print(f'Error getting BTC rate: {e}')