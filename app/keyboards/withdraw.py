from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def withdraw_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Вывести 💸',
                    callback_data='withdraw'
                )
            ]
        ]
    )