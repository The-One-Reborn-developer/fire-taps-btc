from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard() -> ReplyKeyboardMarkup:
    """
    Generates a ReplyKeyboardMarkup for the main keyboard.

    This keyboard is shown to the user as soon as they start the bot.
    It contains the following buttons:
    1. 'Играть' - starts a game.
    2. 'Профиль' - shows the user's profile.

    Returns:
        ReplyKeyboardMarkup with the described buttons.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
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
