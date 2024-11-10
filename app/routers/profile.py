from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.tasks.celery import get_user_by_id_task
from app.tasks.celery import put_user_task
from app.tasks.celery import create_check_task
from app.tasks.celery import convert_btc_to_usdt_task
from app.tasks.celery import get_balance_task

from app.keyboards.profile import profile_keyboard
from app.keyboards.main import main_keyboard


class Profile(StatesGroup):
    update_referral = State()
    withdraw = State()


profile_router = Router()


@profile_router.message(F.text == 'Профиль 👤')
async def profile(message: Message, state: FSMContext) -> None:
    """
    Handles "Профиль" button in main menu. Checks if user is in the database, 
    clears state, deletes message, fetches user data and sends message with 
    user's profile information.

    Args:
        message (Message): The message with the "Профиль" button.
        state (FSMContext): The current state of the user.

    Returns:
        None
    """
    try:
        await state.clear()

        await message.delete()

        user_task = get_user_by_id_task.delay(message.from_user.id)
        user = user_task.get()

        if user[0] is None:
            btc_balance = 0.00000000
        else:
            btc_balance = '{:.8f}'.format(user[0])

        converted_balance_task = convert_btc_to_usdt_task.delay(
            float(btc_balance))
        converted_balance = converted_balance_task.get()

        if converted_balance is None:
            usdt_equivalent = 0.00
        else:
            usdt_equivalent = '{:.2f}'.format(converted_balance)

        referrals_amount = user[1]
        play_referral_code = user[7]
        if play_referral_code is None:
            play_referral_code = 'не установлен'

        if user:
            content = f'Пользователь: {message.from_user.first_name}\n\n' \
                f'BTC Баланс: <code>{btc_balance}</code> ₿\nUSDT эквивалент: {usdt_equivalent} ₮\n\n' \
                f'Количество зарегистрированных рефералов: {referrals_amount}\n\n' \
                f'Код реферала (для регистрации): <code>{user[2]}</code>\n\n' \
                f'Код реферала (для игры): <code>{user[7]}</code>'

            await message.answer(content, reply_markup=profile_keyboard(), parse_mode='HTML')
    except Exception as e:
        print(f'Profile error: {e}')


@profile_router.callback_query(F.data == 'update_referral')
async def update_referral(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Handles "Обновить реферальный код" button in profile menu. Checks if user is in the database, 
    clears state, deletes message, fetches user data and sends message with 
    prompt to enter new referral code.

    Args:
        callback (CallbackQuery): The callback query with the "Обновить реферальный код" button.
        state (FSMContext): The current state of the user.

    Returns:
        None
    """
    try:
        await state.set_state(Profile.update_referral)

        content = 'Введи новый реферальный код 🔑'

        await callback.message.answer(content)
    except Exception as e:
        print(f'Update referral error: {e}')


@profile_router.message(Profile.update_referral)
async def update_referral_new(message: Message, state: FSMContext) -> None:
    """
    Handles message with new referral code in "update_referral" state. Checks if user is in the database, 
    updates user's referral code, clears state, deletes message, and sends message with 
    confirmation of successful update.

    Args:
        message (Message): The message with the new referral code.
        state (FSMContext): The current state of the user.

    Returns:
        None
    """
    try:
        put_user_task.delay(message.from_user.id,
                            play_referral_code=message.text)

        await state.clear()

        content = 'Реферальный код обновлен ✅'

        await message.answer(content, reply_markup=main_keyboard())
    except Exception as e:
        print(f'Update referral error: {e}')


@profile_router.callback_query(F.data == 'withdraw')
async def withdraw(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Handles "Вывести" button in profile menu. Checks if user is in the database, 
    clears state, deletes message, fetches user data and sends message with 
    prompt to enter amount of BTC to withdraw.

    Args:
        callback (CallbackQuery): The callback query with the "Вывести" button.
        state (FSMContext): The current state of the user.

    Returns:
        None
    """
    try:
        await state.set_state(Profile.withdraw)

        content = 'Введи количество BTC для вывода.'

        await callback.message.answer(content)
    except Exception as e:
        print(f'Withdraw error: {e}')


@profile_router.message(Profile.withdraw)
async def withdraw_btc(message: Message, state: FSMContext) -> None:
    """
    Handles message with amount of BTC to withdraw in "withdraw" state. Checks if user is in the database, 
    checks if user has enough balance to withdraw, checks if app has enough balance to withdraw, 
    creates a check, updates user's balance, sends message with check information, and clears state.

    Args:
        message (Message): The message with the amount of BTC to withdraw.
        state (FSMContext): The current state of the user.

    Returns:
        None
    """
    try:
        get_user_task = get_user_by_id_task.delay(message.from_user.id)
        user = get_user_task.get()
        btc_balance = user[0]

        app_balance_task = get_balance_task.delay()
        app_balance = app_balance_task.get()

        converted_withdraw_task = convert_btc_to_usdt_task.delay(
            float(message.text))
        converted_withdraw = converted_withdraw_task.get()

        if btc_balance < float(message.text):
            content = 'Твой баланс меньше введенной суммы. Попробуй ещё раз 🙂'

            await message.answer(content)
        elif app_balance < converted_withdraw:
            content = 'Ошибка при выводе. Попробуй ещё раз 🙂'

            await message.answer(content)
        else:
            check_task = create_check_task.delay(converted_withdraw)
            check = check_task.get()
            print(check)
            if check == 400:
                await message.answer('Введи сумму эквивалентную или больше 0.02 $ USD 😉')

                return

            content = f'Чек {check['check_id']} на сумму {'{:.8f}'.format(check['amount'])} {check['asset']} создан в {check['created_at']} ✅\n' \
                f'Активация по ссылке: {check['bot_check_url']}'

            put_user_task.delay(message.from_user.id,
                                btc_balance=btc_balance - float(message.text))

            await message.answer(content, reply_markup=main_keyboard())

            await state.clear()
    except Exception as e:
        print(f'Withdraw BTC error: {e}')
