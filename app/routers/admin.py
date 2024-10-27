from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from app.database.queues.get_user import get_user

from app.bot.get_balance import get_balance

from app.generators.play_referral import play_referral

from app.keyboards.admin import admin_keyboard
from app.keyboards.main import main_keyboard


admin_router = Router()


@admin_router.message(Command('admin'))
async def admin_panel(message: Message) -> None:
    try:
        user = await get_user(message.from_user.id)

        if user[5] is True:
            await message.delete()

            balance = await get_balance()

            with open('app/temp/play_referral_code.txt', 'r') as f:
                play_referral_code = f.read()

            content = 'Вход в панель администратора 🔑\n' \
                      f'Баланс BTC кошелька приложения: {balance} ₿\n' \
                      f'Текущий реферальный код для игры: {play_referral_code}'

            await message.answer(content, reply_markup=admin_keyboard())
        else:
            await message.answer('Ошибка входа в панель администратора ❌')
    except Exception as e:
        print(f'Admin panel error: {e}')


@admin_router.message(F.text == 'Выйти из админ панели 🔙')
async def exit_admin_panel(message: Message) -> None:
    try:
        user = await get_user(message.from_user.id)

        if user[5] is True:
            await message.delete()

            await message.answer('Вы вышли из панели администратора ✅', reply_markup=main_keyboard())
        else:
            pass
    except Exception as e:
        print(f'Exit admin panel error: {e}')


@admin_router.message(F.text == 'Сгенерировать реф. код для игры 🎁')
async def generate_referral_code(message: Message) -> None:
    try:
        user = await get_user(message.from_user.id)

        if user[5] is True:
            await message.delete()

            await play_referral()

            balance = await get_balance()

            with open('app/temp/play_referral_code.txt', 'r') as f:
                play_referral_code = f.read()

            content = f'Баланс BTC кошелька приложения: {balance} ₿\n' \
                      f'Текущий реферальный код для игры: {play_referral_code}'

            await message.answer(content, reply_markup=admin_keyboard())
        else:
            pass
    except Exception as e:
        print(f'Generate referral code error: {e}')


@admin_router.message(F.text == 'Пополнить BTC кошелёк ₿')
async def deposit_btc(message: Message) -> None:
    try:
        user = await get_user(message.from_user.id)

        if user[5] is True:
            await message.delete()

            pass
        else:
            pass
    except Exception as e:
        print(f'Deposit BTC error: {e}')