from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.database.queues.get_user_by_id import get_user_by_id
from app.database.queues.put_user import put_user

from app.bot.create_check import create_check

from app.keyboards.profile import profile_keyboard


class Profile(StatesGroup):
    update_referral = State()
    withdraw = State()


profile_router = Router()


@profile_router.message(F.text == 'Профиль 👤')
async def profile(message: Message, state: FSMContext) -> None:
    try:
        await state.clear()

        await message.delete()
        
        user = await get_user_by_id(message.from_user.id)
        
        btc_balance = '{:.8f}'.format(user[0])
        referrals_amount = user[1]
        play_referral_code = user[7]
        if play_referral_code is None:
            play_referral_code = 'не установлен'

        if user:
            content = f'Пользователь: {message.from_user.first_name}\n\n' \
                    f'BTC Баланс: {btc_balance} ₿\n\n' \
                    f'Количество зарегистрированных рефералов: {referrals_amount}\n\n' \
                    f'Код реферала (для регистрации): <code>{user[2]}</code>\n\n' \
                    f'Код реферала (для игры): <code>{user[7]}</code>'

            await message.answer(content, reply_markup=profile_keyboard(), parse_mode='HTML')
    except Exception as e:
        print(f'Profile error: {e}')


@profile_router.callback_query(F.data == 'update_referral')
async def update_referral(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        await state.set_state(Profile.update_referral)

        content = 'Введите новый реферальный код 🔑'

        await callback.message.answer(content)
    except Exception as e:
        print(f'Update referral error: {e}')


@profile_router.message(Profile.update_referral)
async def update_referral_new(message: Message, state: FSMContext) -> None:
    try:
        await put_user(message.from_user.id, play_referral_code=message.text)

        await state.clear()

        content = 'Реферальный код обновлен ✅'

        await message.answer(content)
    except Exception as e:
        print(f'Update referral error: {e}')


@profile_router.callback_query(F.data == 'withdraw')
async def withdraw(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        await state.set_state(Profile.withdraw)

        content = 'Введите количество BTC для вывода.'

        await callback.message.answer(content)
    except Exception as e:
        print(f'Withdraw error: {e}')

    
@profile_router.message(Profile.withdraw)
async def withdraw_btc(message: Message, state: FSMContext) -> None:
    try:
        user = await get_user_by_id(message.from_user.id)
        user_balance = user[0]

        if user_balance < float(message.text):
            content = 'Ваш баланс меньше введенной суммы. Попробуйте ещё раз 🙂'

            await message.answer(content)
        else:
            check = await create_check(message.text)
            if check == 400:
                await message.answer('Введите сумму эквивалентную или больше 0.02 $ USD 😉')

                return

            content = f'Чек {check.check_id} на сумму {'{:.8f}'.format(check.amount)} {check.asset} создан в {check.created_at} ✅\n' \
                    f'Активация по ссылке: {check.bot_check_url}'
            
            await put_user(message.from_user.id, btc_balance=user_balance - float(message.text))
            
            await message.answer(content)

            await state.clear()
    except Exception as e:
        print(f'Withdraw BTC error: {e}')