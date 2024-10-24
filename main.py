import os
import asyncio

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv, find_dotenv

from app.routers.start import start_router
from app.database.queues.create_tables import create_tables


load_dotenv(find_dotenv())


async def on_startup() -> None:
    try:
        await create_tables()
    except Exception as e:
        print(f'Error creating tables: {e}')

    bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(start_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(on_startup())