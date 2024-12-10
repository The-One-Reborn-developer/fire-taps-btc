import os

from aiocpa import CryptoPay, TESTNET, MAINNET

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


crypto_bot = CryptoPay(os.getenv('CRYPTO_BOT_TOKEN'), api_server=MAINNET)