from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart

from app.database.queues.get_user import get_user
from app.database.queues.post_user import post_user
from app.database.queues.put_user import put_user

from app.keyboards.start import start_keyboard


start_router = Router()


@start_router.message(CommandStart())
async def start_command(message: Message) -> None:
    telegram_id = message.from_user.id
    try:
        user = await get_user(telegram_id)
    except Exception as e:
        print(f'Error getting user: {e}')

    if not user:
        try:
            await post_user(telegram_id)
        except Exception as e:
            print(f'Error creating user: {e}')

    content = 'Приветствую 👋\nДобро пожаловать в Bitcoin кран от Fire Taps.\n' \
              'Только тут ты сможешь зарабатывать реальные деньги 💰 не вкладывая свои!\n' \
              'Зови друзей в игру и получайте вместе ещё больше монет 🤵‍♂️🤵\n\n' \
              'Чтобы начать нажми на кнопку внизу 👇'
    
    await message.answer(content, reply_markup=start_keyboard())


@start_router.message()
async def contact_handler(message: Message) -> None:
    phone_number = message.contact.phone_number
    telegram_id = message.from_user.id

    try:
        await put_user(telegram_id, phone=phone_number)

        content = 'Вы зарегистрированы, можете пользоваться ботом 🙂'

        await message.delete()

        await message.answer(content, reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        print(f'Error updating user`s phone: {e}')

        content = 'Ошибка при регистрации, попробуйте ещё раз 😕'

        await message.delete()

        await message.answer(content, reply_markup=ReplyKeyboardRemove())