from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.tasks.celery import get_user_by_id_task
from app.tasks.celery import get_user_by_registration_referral_task
from app.tasks.celery import post_user_task
from app.tasks.celery import put_user_task

from app.keyboards.start import start_keyboard
from app.keyboards.main import main_keyboard

from app.generators.registration_referral import registration_referral


class Registration(StatesGroup):
    start = State()
    contact = State()
    referral = State()


start_router = Router()

'''
@start_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    """
    Handles the /start command.

    If the user is not in the database, creates a new user, generates a registration referral code,
    and sends a welcome message to the user.

    If the user is already in the database, clears the state, and sends a message to the user
    with a link to the main menu.

    Args:
        message (Message): The message with the /start command.
        state (FSMContext): The current state of the user.

    Returns:
        None
    """
    #await state.set_state(Registration.start)

    telegram_id = message.from_user.id
    try:
        user_task = get_user_by_id_task.delay(telegram_id)
        user = user_task.get()
    except Exception as e:
        print(f'Error getting user: {e}')

    if not user:
        try:
            post_user_task.delay(telegram_id)

            generated_registration_referral = await registration_referral()

            with open('app/temp/admin_list.txt', 'r') as f:
                admins = f.read().splitlines()

            if str(telegram_id) in admins:
                put_user_task.delay(
                    telegram_id, registration_referral_code=generated_registration_referral, is_admin=True)
            else:
                put_user_task.delay(
                    telegram_id, registration_referral_code=generated_registration_referral)

            content = 'Приветствую 👋\nДобро пожаловать в Bitcoin кран от Fire Taps.\n' \
                'Только тут ты сможешь зарабатывать реальные деньги 💰 не вкладывая свои!\n' \
                'Зови друзей в игру и получайте вместе ещё больше монет 🤵‍♂️🤵\n\n' \
                #'Чтобы начать нажми на кнопку внизу 👇'

            #await state.set_state(Registration.contact)
            await state.set_state(Registration.referral)
            #await message.answer(content, reply_markup=start_keyboard())
        except Exception as e:
            print(f'Error creating user: {e}')

            content = 'Произошла ошибка, попробуй ещё раз или обратись в поддержку 😕'

            await message.answer(content)
    else:
        await state.clear()

        content = 'Ты уже зарегистрирован, можешь пользоваться ботом 🙂'

        await message.answer(content, reply_markup=main_keyboard())

'''
@start_router.message(CommandStart())
async def contact_handler(message: Message, state: FSMContext) -> None:
    """
    Handles the contact message in the Registration.contact state. Updates the user`s phone in the database,
    sends the message with the prompt to enter the referral code, and sets the state to Registration.referral.
    If any error occurs, sends the message with the error text and sets the state back to the start state.

    Args:
        message (Message): The message with the contact information.
        state (FSMContext): The current state of the user.

    Returns:
        None
    """
    #phone_number = message.contact.phone_number
    telegram_id = message.from_user.id

    try:
        #put_user_task.delay(telegram_id, phone=phone_number)
        put_user_task.delay(telegram_id)
        content = 'Приветствую 👋\nДобро пожаловать в Bitcoin кран от Fire Taps.\n' \
                'Только тут ты сможешь зарабатывать реальные деньги 💰 не вкладывая свои!\n' \
                'Зови друзей в игру и получайте вместе ещё больше монет 🤵‍♂️🤵\n\n' \
                'Введи реферальный код для завершения регистрации 🔑'

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
    """
    Handles the referral code message in the Registration.referral state. Checks if the referral code exists in the database,
    sends the message with the result of the check, and sets the state back to the start state.
    If any error occurs, sends the message with the error text and sets the state back to the start state.

    Args:
        message (Message): The message with the referral code.
        state (FSMContext): The current state of the user.

    Returns:
        None
    """
    referral_code = message.text

    await message.delete()

    try:
        user_found_task = get_user_by_registration_referral_task.delay(
            referral_code)
        user_found = user_found_task.get()

        if user_found is True:
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
