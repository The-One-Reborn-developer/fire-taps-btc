from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.database.queues.get_user_by_id import get_user_by_id
from app.database.queues.put_user import put_user

from app.keyboards.profile import profile_keyboard


class UpdateReferral(StatesGroup):
    update_referral = State()


profile_router = Router()


@profile_router.message(F.text == 'Профиль 👤')
async def profile(message: Message, state: FSMContext) -> None:
    try:
        await state.clear()

        await message.delete()
        
        user = await get_user_by_id(message.from_user.id)
        
        if user[0] is None:
            btc_balance = 0
        else:
            btc_balance = '{:.8f}'.format(user[0])

        if user[1] is None:
            referrals_amount = 0
        else:
            referrals_amount = user[1]

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
        await state.set_state(UpdateReferral.update_referral)

        content = 'Введите новый реферальный код 🔑'

        await callback.message.answer(content)
    except Exception as e:
        print(f'Update referral error: {e}')


@profile_router.message(UpdateReferral.update_referral)
async def update_referral_new(message: Message, state: FSMContext) -> None:
    try:
        await put_user(message.from_user.id, play_referral_code=message.text)

        await state.clear()

        content = 'Реферальный код обновлен ✅'

        await message.answer(content)
    except Exception as e:
        print(f'Update referral error: {e}')