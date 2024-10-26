from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup (
        keyboard = [
            [
                KeyboardButton(
                    text='Играть 💸'
                )
            ],
            [
                KeyboardButton(
                    text='Профиль 👤',
                    callback_data='profile'
                )
            ]
        ],
        resize_keyboard=True
    )