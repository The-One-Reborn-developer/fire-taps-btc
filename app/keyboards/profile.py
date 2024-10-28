from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def profile_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Вывести 💸',
                    callback_data='withdraw'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Обновить реферальный код 🔄',
                    callback_data='update_referral'
                )
            ]
        ]
    )