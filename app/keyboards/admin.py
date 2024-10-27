from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup (
        keyboard = [
            [
                KeyboardButton(
                    text='Сгенерировать реф. код для игры 🎁'
                )
            ],
            [
                KeyboardButton(
                    text='Пополнить BTC кошелёк ₿'
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