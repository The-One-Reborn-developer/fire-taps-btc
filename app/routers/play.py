import time

from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.queues.get_user_by_id import get_user_by_id
from app.database.queues.put_user import put_user
from app.database.queues.get_user_by_play_referral import get_user_by_play_referral

from app.generators.waiting_time import waiting_time
from app.generators.rubles import rubles

from app.bot.get_btc_rate import get_btc_rate


play_router = Router()


@play_router.message(F.text == 'Играть 💸')
async def check_referral_code(message: Message, state: FSMContext) -> None:
    try:
        await state.clear()

        await message.delete()

        user_play_referral_code = await get_user_by_play_referral(message.from_user.id)

        if user_play_referral_code:
            pass
        else:
            content = 'Твоя реферальная ссылка неактуальна, ты не сможешь получить криптовалюту.\n' \
                      'Получи актуальную ссылку в 👉<a href="https://www.google.com">канале</a>👈'
            
            await message.answer(content, parse_mode='HTML')

            return None

        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        user = await get_user_by_id(message.from_user.id)

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
            generated_btc = round((generated_rubles / await get_btc_rate()), 8)
            formatted_generated_crypto = '{:.8f}'.format(generated_btc)

            await put_user(message.from_user.id, btc_balance=user[0] + generated_btc, number_of_plays=user[6] + 1)

            content = f'Ты получил {formatted_generated_crypto} ₿'

            await message.answer(content)

            await put_user(message.from_user.id, last_played=now)
    except Exception as e:
        print(f'Play error: {e}')

        content = 'Произошла ошибка, попробуй ещё раз или обратись в поддержку 😕'

        await message.answer(content)