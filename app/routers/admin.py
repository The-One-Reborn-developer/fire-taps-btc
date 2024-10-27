from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

from app.database.queues.get_user import get_user

from app.keyboards.admin import admin_keyboard


admin_router = Router()


@admin_router.message(Command('admin'))
async def admin_panel(message: Message) -> None:
    try:
        user = await get_user(message.from_user.id)

        if user[5] is True:
            await message.answer('Вход в панель администратора ✅', reply_markup=admin_keyboard())
        else:
            await message.answer('Ошибка входа в панель администратора ❌')
    except Exception as e:
        print(f'Admin panel error: {e}')