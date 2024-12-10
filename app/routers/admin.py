from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiocpa.types import Invoice

from app.bot.crypto_bot import crypto_bot

from app.tasks.celery import get_balance_task
from app.tasks.celery import get_user_by_id_task

from app.generators.play_referral import play_referral

from app.keyboards.admin import admin_keyboard
from app.keyboards.main import main_keyboard


class Deposit(StatesGroup):
    amount = State()


admin_router = Router()


@admin_router.message(Command('admin'))
async def admin_panel(message: Message, state: FSMContext) -> None:
    """
    Handles /admin command. Checks if user is admin and shows admin panel with bot`s balance and current referral code.

    Args:
        message (Message): Message object.
        state (FSMContext): FSMContext object.

    Returns:
        None
    """
    try:
        user_task = get_user_by_id_task.delay(message.from_user.id)
        user = user_task.get()

        if user[5] is True:
            await message.delete()

            balance_task = get_balance_task.delay()
            balance = balance_task.get()

            if balance is None:
                formatted_balance = 0.00
            else:
                formatted_balance = '{:.2f}'.format(balance)

            with open('app/temp/play_referral_code.txt', 'r') as f:
                play_referral_code = f.read()

            await state.clear()

            content = 'Вход в панель администратора 🔑\n' \
                      f'Баланс USDT кошелька приложения: {formatted_balance} ₮\n' \
                      f'Текущий реферальный код для игры: <code>{
                          play_referral_code}</code>'

            await message.answer(content, reply_markup=admin_keyboard(), parse_mode='HTML')
        else:
            await message.answer('Ошибка входа в панель администратора ❌')
    except Exception as e:
        print(f'Admin panel error: {e}')


@admin_router.message(F.text == 'Выйти из админ панели 🔙')
async def exit_admin_panel(message: Message, state: FSMContext) -> None:
    """
    Handles "Выйти из админ панели" button in admin panel. Checks if user is admin, clears state and sends message about exiting the admin panel.

    Args:
        message (Message): Message object.
        state (FSMContext): FSMContext object.

    Returns:
        None
    """
    try:
        user_task = get_user_by_id_task.delay(message.from_user.id)
        user = user_task.get()

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
    """
    Handles "Сгенерировать реф. код для игры" button in admin panel. Checks if user is admin, generates new referral code,
    clears state and sends message about new referral code.

    Args:
        message (Message): Message object.
        state (FSMContext): FSMContext object.

    Returns:
        None
    """
    try:
        user_task = get_user_by_id_task.delay(message.from_user.id)
        user = user_task.get()

        if user[5] is True:
            await message.delete()

            await play_referral()

            balance_task = get_balance_task.delay()
            balance = balance_task.get()
            formatted_balance = '{:.2f}'.format(balance)

            with open('app/temp/play_referral_code.txt', 'r') as f:
                play_referral_code = f.read()

            await state.clear()

            content = f'Баланс USDT кошелька приложения: {formatted_balance} ₮\n' \
                f'Текущий реферальный код для игры: <code>{
                    play_referral_code}</code>'

            await message.answer(content, reply_markup=admin_keyboard(), parse_mode='HTML')
        else:
            pass
    except Exception as e:
        print(f'Generate referral code error: {e}')


@admin_router.message(F.text == 'Пополнить USDT кошелёк ₮')
async def deposit_btc(message: Message, state: FSMContext) -> None:
    """
    Handles "Пополнить USDT кошелёк" button in admin panel. Checks if user is admin,
    prompts for USDT amount to deposit, and sets the state for the deposit transaction.

    Args:
        message (Message): Message object.
        state (FSMContext): FSMContext object.

    Returns:
        None
    """
    try:
        user_task = get_user_by_id_task.delay(message.from_user.id)
        user = user_task.get()

        if user[5] is True:
            await message.delete()

            content = 'Введите количество USDT для пополнения.'

            await state.set_state(Deposit.amount)

            await message.answer(content)
        else:
            pass
    except Exception as e:
        print(f'Deposit BTC error: {e}')


@admin_router.message(Deposit.amount)
async def deposit_btc_amount(message: Message, state: FSMContext) -> None:
    """
    Handles user input for USDT amount to deposit. Checks if user is admin,
    updates state with the given amount, creates an invoice for the given amount,
    and sends a message with the invoice link to the user.

    The invoice is then awaited for payment using the invoice.await_payment method.
    If the invoice is paid, the state is cleared and the user is returned to the
    admin panel.

    If the user is not an admin, the message is simply deleted and no action is taken.

    If an exception occurs during this process, the error code is checked and if it
    is 400 (validation error), the user is sent a message with a hint to enter a
    valid amount.

    Args:
        message (Message): Message object.
        state (FSMContext): FSMContext object.

    Returns:
        None
    """
    try:
        user_task = get_user_by_id_task.delay(message.from_user.id)
        user = user_task.get()

        if user[5] is True:
            await message.delete()

            await state.update_data(amount=message.text)

            amount = await state.get_data()

            invoice = await crypto_bot.create_invoice(amount['amount'], 'USDT')

            await message.answer(f'Оплатите {amount["amount"]} USDT по ссылке в CryptoTestnetBot (тестовый счёт){invoice.mini_app_invoice_url}',
                                 reply_markup=admin_keyboard())

            invoice.await_payment(message=message, state=state)
        else:
            pass
    except Exception as e:
        print(f'Deposit USDT amount error: {e}')

        error_code = int(str(e).split(' ')[0].strip('[]'))
        if error_code == 400:
            await message.answer('Введите сумму эквивалентную или больше 0.01 $ USD 😉')


@crypto_bot.polling_handler()
async def handle_payment(invoice: Invoice, message: Message) -> None:
    """
    Handles the payment event when an invoice is paid. Sends a confirmation
    message to the user indicating the successful payment of the specified 
    amount and asset.

    Args:
        invoice (Invoice): The invoice that was paid.
        message (Message): The message that triggered the payment event.

    Returns:
        None
    """
    await message.answer(f'Платеж {invoice.amount} {invoice.asset} успешно оплачён 🙂')
