from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from cryptopay.types import Invoice

from app.database.queues.get_user import get_user

from app.bot.crypto_bot import crypto_bot
from app.bot.get_balance import get_balance

from app.generators.play_referral import play_referral

from app.keyboards.admin import admin_keyboard
from app.keyboards.main import main_keyboard


class Deposit(StatesGroup):
    amount = State()


admin_router = Router()


@admin_router.message(Command('admin'))
async def admin_panel(message: Message, state: FSMContext) -> None:
    try:
        user = await get_user(message.from_user.id)

        if user[5] is True:
            await message.delete()

            balance = await get_balance()
            formatted_balance = '{:.8f}'.format(balance)

            with open('app/temp/play_referral_code.txt', 'r') as f:
                play_referral_code = f.read()

            await state.clear()

            content = 'Вход в панель администратора 🔑\n' \
                      f'Баланс BTC кошелька приложения: {formatted_balance} ₿\n' \
                      f'Текущий реферальный код для игры: {play_referral_code}'

            await message.answer(content, reply_markup=admin_keyboard())
        else:
            await message.answer('Ошибка входа в панель администратора ❌')
    except Exception as e:
        print(f'Admin panel error: {e}')


@admin_router.message(F.text == 'Выйти из админ панели 🔙')
async def exit_admin_panel(message: Message, state: FSMContext) -> None:
    try:
        user = await get_user(message.from_user.id)

        if user[5] is True:
            await message.delete()

            await state.clear()

            await message.answer('Вы вышли из панели администратора ✅', reply_markup=main_keyboard())
        else:
            pass
    except Exception as e:
        print(f'Exit admin panel error: {e}')


@admin_router.message(F.text == 'Сгенерировать реф. код для игры 🎁')
async def generate_referral_code(message: Message, state: FSMContext) -> None:
    try:
        user = await get_user(message.from_user.id)

        if user[5] is True:
            await message.delete()

            await play_referral()

            balance = await get_balance()
            formatted_balance = '{:.8f}'.format(balance)

            with open('app/temp/play_referral_code.txt', 'r') as f:
                play_referral_code = f.read()

            await state.clear()

            content = f'Баланс BTC кошелька приложения: {formatted_balance} ₿\n' \
                      f'Текущий реферальный код для игры: {play_referral_code}'

            await message.answer(content, reply_markup=admin_keyboard())
        else:
            pass
    except Exception as e:
        print(f'Generate referral code error: {e}')


@admin_router.message(F.text == 'Пополнить BTC кошелёк ₿')
async def deposit_btc(message: Message, state: FSMContext) -> None:
    try:
        user = await get_user(message.from_user.id)

        if user[5] is True:
            await message.delete()

            content = 'Введите количество BTC для пополнения.'

            await state.set_state(Deposit.amount)

            await message.answer(content)
        else:
            pass
    except Exception as e:
        print(f'Deposit BTC error: {e}')


@admin_router.message(Deposit.amount)
async def deposit_btc_amount(message: Message, state: FSMContext) -> None:
    try:
        user = await get_user(message.from_user.id)

        if user[5] is True:
            await message.delete()

            await state.update_data(amount=message.text)

            amount = await state.get_data()

            invoice = await crypto_bot.create_invoice(amount['amount'], 'BTC')

            await message.answer(f'Оплатите {amount["amount"]} BTC по ссылке в CryptoTestnetBot (тестовый счёт){invoice.mini_app_invoice_url}')

            invoice.await_payment(message=message, state=state)
        else:
            pass
    except Exception as e:
        print(f'Deposit BTC amount error: {e}')

        error_code = int(str(e).split(' ')[0].strip('[]'))
        if error_code == 400:
            await message.answer('Введите сумму эквивалентную или больше 0.01 $ USD 😉')


@crypto_bot.polling_handler()
async def handle_payment(invoice: Invoice, message: Message) -> None:
    await message.answer(f'Платеж {invoice.amount} {invoice.asset} успешно оплачён 🙂')