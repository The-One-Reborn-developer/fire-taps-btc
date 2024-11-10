from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_keyboard() -> ReplyKeyboardMarkup:
    """
    Generates a ReplyKeyboardMarkup for the start command.

    This keyboard is shown to the user when they start the bot.
    It contains the following button:
    1. 'Зарегистрироваться ' - starts the registration process.
    The button asks for the user's contact information.

    Returns: 
        ReplyKeyboardMarkup with the described button.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Зарегистрироваться 📲',
                               request_contact=True)
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
