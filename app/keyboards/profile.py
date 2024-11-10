from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def profile_keyboard() -> InlineKeyboardMarkup:
    """
    Generates an InlineKeyboardMarkup for the profile section.

    This keyboard is displayed to the user within their profile section and 
    contains the following buttons:
    1. 'Вывести' - initiates a withdrawal process.
    2. 'Обновить реферальный код' - starts the process to update the referral code.

    Returns: 
        InlineKeyboardMarkup with the described buttons.
    """
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
