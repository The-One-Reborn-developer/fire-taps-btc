from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.database.queues.get_user_by_id import get_user_by_id
from app.database.queues.get_user_by_registration_referral import get_user_by_registration_referral
from app.database.queues.post_user import post_user
from app.database.queues.put_user import put_user

from app.keyboards.start import start_keyboard
from app.keyboards.main import main_keyboard

from app.generators.registration_referral import registration_referral


class Registration(StatesGroup):
    start = State()
    contact = State()
    referral = State()


start_router = Router()


@start_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    await state.set_state(Registration.start)

    telegram_id = message.from_user.id
    try:
        user = await get_user_by_id(telegram_id)
    except Exception as e:
        print(f'Error getting user: {e}')

    if not user:
        try:
            await post_user(telegram_id)

            generated_registration_referral = await registration_referral()

            if telegram_id == 7167827272:
                await put_user(telegram_id, registration_referral_code=generated_registration_referral, is_admin=True)
            else:
                await put_user(telegram_id, registration_referral_code=generated_registration_referral)

            content = 'Приветствую 👋\nДобро пожаловать в Bitcoin кран от Fire Taps.\n' \
              'Только тут ты сможешь зарабатывать реальные деньги 💰 не вкладывая свои!\n' \
              'Зови друзей в игру и получайте вместе ещё больше монет 🤵‍♂️🤵\n\n' \
              'Чтобы начать нажми на кнопку внизу 👇'
            
            await state.set_state(Registration.contact)
            
            await message.answer(content, reply_markup=start_keyboard())
        except Exception as e:
            print(f'Error creating user: {e}')

            content = 'Произошла ошибка, попробуй ещё раз или обратись в поддержку 😕'

            await message.answer(content)
    else:
        await state.clear()

        content = 'Ты уже зарегистрирован, можешь пользоваться ботом 🙂'

        await message.answer(content, reply_markup=main_keyboard())
    


@start_router.message(Registration.contact)
async def contact_handler(message: Message, state: FSMContext) -> None:
    phone_number = message.contact.phone_number
    telegram_id = message.from_user.id

    try:
        await put_user(telegram_id, phone=phone_number)

        content = 'Введи реферальный код для завершения регистрации 🔑'

        await message.delete()

        await message.answer(content)

        await state.set_state(Registration.referral)
    except Exception as e:
        print(f'Error updating user`s phone: {e}')

        content = 'Ошибка при регистрации, попробуй ещё раз 😕'

        await message.delete()

        await message.answer(content, reply_markup=start_keyboard())


@start_router.message(Registration.referral)
async def registration_referral_code_handler(message: Message, state: FSMContext) -> None:
    referral_code = message.text

    await message.delete()

    try:
        user_found = await get_user_by_registration_referral(referral_code)

        if user_found:
            content = 'Ты зарегистрирован, можешь пользоваться ботом 🙂'

            await message.answer(content, reply_markup=main_keyboard())

            await state.clear()
        else:
            content = 'Такого реферального кода не существует, попробуй ещё раз 😕'

            await message.answer(content, reply_markup=start_keyboard())
    except Exception as e:
        print(f'Error updating user`s phone: {e}')

        content = 'Ошибка при регистрации, попробуй ещё раз 😕'

        await message.delete()

        await message.answer(content, reply_markup=start_keyboard())