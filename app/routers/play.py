import time

from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message

from app.database.queues.get_user import get_user
from app.database.queues.put_user import put_user

from app.generators.waiting_time import waiting_time
from app.generators.rubles import rubles

from app.scripts.get_btc_rate import get_btc_rate

play_router = Router()


@play_router.message(F.text == 'Играть 💸')
async def play(message: Message) -> None:
    try:
        await message.delete()

        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        user = await get_user(message.from_user.id)

        if user[3] is not None and user[3] > one_hour_ago:
            time_since_last_play = now - user[3]
            minutes_until_next_play = 60 - int(time_since_last_play.total_seconds() // 60)

            content = f'Вы уже играли в этот час, попробуйте через {minutes_until_next_play} минут 😊'

            await message.answer(content)
        else:
            await put_user(message.from_user.id, last_played=now)

            content = 'Получаем криптовалюту, нужно немного подождать ⏳'

            await message.answer(content)

            time.sleep(await waiting_time())

            generated_rubles = await rubles(user[4])
            generated_crypto = round((generated_rubles / await get_btc_rate()), 8)
            formatted_generated_crypto = '{:.8f}'.format(generated_crypto)

            if user[0] is None:
                await put_user(message.from_user.id, btc_balance=generated_crypto)
            else:
                await put_user(message.from_user.id, btc_balance=user[0] + formatted_generated_crypto)

            content = f'Вы получили {formatted_generated_crypto} ₿ из {generated_rubles} ₽'

            await message.answer(content)
    except Exception as e:
        print(f'Play error: {e}')