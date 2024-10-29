import time

from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.tasks.celery import get_user_by_id_task
from app.tasks.celery import put_user_task
from app.tasks.celery import get_user_by_play_referral_task
from app.tasks.celery import get_btc_rate_task

from app.generators.waiting_time import waiting_time
from app.generators.rubles import rubles


play_router = Router()


@play_router.message(F.text == 'Играть 💸')
async def check_referral_code(message: Message, state: FSMContext) -> None:
    """
    Checks if the user's referral code is valid and not expired.

    If the referral code is invalid or expired, the user cannot play and will be notified.
    If the referral code is valid and not expired, the user can play and will be notified of how long they have to wait before they can play again.

    Args:
        message (Message): The message that triggered this function.
        state (FSMContext): The current state of the user.

    Returns:
        None
    """
    try:
        await state.clear()

        await message.delete()

        user_play_referral_code_task = get_user_by_play_referral_task.delay(message.from_user.id)
        user_play_referral_code = user_play_referral_code_task.get()

        if user_play_referral_code:
            pass
        else:
            content = 'Твоя реферальная ссылка неактуальна, ты не сможешь получить криптовалюту.\n' \
                      'Получи актуальную ссылку в 👉<a href="https://www.google.com">канале</a>👈'
            
            await message.answer(content, parse_mode='HTML')

            return None

        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        user_task = get_user_by_id_task.delay(message.from_user.id)
        user = user_task.get()

        if user[3] is not None and user[3] > one_hour_ago:
            time_since_last_play = now - user[3]
            minutes_until_next_play = 60 - int(time_since_last_play.total_seconds() // 60)

            content = f'Ты уже играл в этот час, попробуй через {minutes_until_next_play} минут 😊'

            await message.answer(content)
        else:
            content = 'Получаем криптовалюту, нужно немного подождать ⏳'

            await message.answer(content)

            time.sleep(await waiting_time())

            generated_rubles = await rubles(user[4])
            btc_rate_task = get_btc_rate_task.delay()
            btc_rate = btc_rate_task.get()
            generated_btc = round((generated_rubles / btc_rate), 8)
            formatted_generated_crypto = '{:.8f}'.format(generated_btc)

            put_user_task.delay(message.from_user.id, btc_balance=user[0] + generated_btc, number_of_plays=user[6] + 1)

            if user[6] > 25 and user[6] < 50:
                put_user_task.delay(message.from_user.id, level=2)
            elif user[6] > 50:
                put_user_task.delay(message.from_user.id, level=3)

            content = f'Ты получил {formatted_generated_crypto} ₿'

            await message.answer(content)

            put_user_task.delay(message.from_user.id, last_played=now)
    except Exception as e:
        print(f'Play error: {e}')

        content = 'Произошла ошибка, попробуй ещё раз или обратись в поддержку 😕'

        await message.answer(content)