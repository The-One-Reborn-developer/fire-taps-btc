from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Зарегистрироваться 📲', request_contact=True)
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )