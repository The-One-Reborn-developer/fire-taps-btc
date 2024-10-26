from aiogram import Router, F
from aiogram.types import Message

from app.database.queues.get_user import get_user

from app.keyboards.withdraw import withdraw_keyboard


profile_router = Router()


@profile_router.message(F.text == 'Профиль 👤')
async def profile(message: Message) -> None:
    await message.delete()
    
    user = await get_user(message.from_user.id)
    if user[1] is None:
        btc_balance = 0
    if user[2] is None:
        referrals_amount = 0

    if user:
        content = f'Пользователь: {message.from_user.first_name}\n\n' \
                  f'BTC Баланс: {btc_balance} ₿\n\n' \
                  f'Количество зарегистрированных рефералов: {referrals_amount}\n\n' \
                  f'Код реферала (для регистрации): <code>{user[3]}</code>'

        await message.answer(content, reply_markup=withdraw_keyboard(), parse_mode='HTML')