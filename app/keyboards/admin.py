from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_keyboard() -> ReplyKeyboardMarkup:
    """
    Generates a ReplyKeyboardMarkup for the admin panel.

    This keyboard is available only to the administrator of the bot.
    It contains the following buttons:
    1. 'Сгенерировать реф. код для игры ' - generates a new referral code for the game.
    2. 'Пополнить USDT кошелёк ' - replenishes the USDT wallet of the bot.
    3. 'Выйти из админ панели ' - exits the admin panel.

    Returns:
        ReplyKeyboardMarkup with the described buttons.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text='Сгенерировать реф. код для игры 🎁'
                )
            ],
            [
                KeyboardButton(
                    text='Пополнить USDT кошелёк ₮'
                )
            ],
            [
                KeyboardButton(
                    text='Выйти из админ панели 🔙'
                )
            ]
        ],
        resize_keyboard=True
    )
