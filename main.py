import os
import asyncio

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv, find_dotenv

from app.routers.start import start_router
from app.routers.profile import profile_router
from app.routers.play import play_router
from app.routers.admin import admin_router

from app.tasks.celery import create_tables_task


load_dotenv(find_dotenv())


async def on_startup() -> None:
    """
    Starts the bot.

    This function creates all database tables if they don't already exist, and then starts the bot.

    Returns:
        None
    """
    create_tables_task.delay()

    try:
        bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
        dp = Dispatcher()
        dp.include_routers(start_router,
                           profile_router,
                           play_router,
                           admin_router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        print(f'Error starting bot: {e}')


if __name__ == '__main__':
    asyncio.run(on_startup())