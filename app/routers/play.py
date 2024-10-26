import time

from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message

from app.database.queues.get_user import get_user
from app.database.queues.put_user import put_user

from app.generators.waiting_time import waiting_time
from app.generators.btc import btc


play_router = Router()


@play_router.message(F.text == 'Играть 💸')
async def play(message: Message) -> None:
    try:
        await message.delete()

        timestamp = datetime.now().timestamp()
        user = await get_user(message.from_user.id)

        if user[3] is not None and timestamp - user[3] < timedelta(hours=1).total_seconds():
            await message.answer('Вы уже играли в этом часу, попробуйте позже 😊')
        else:
            await put_user(message.from_user.id, last_played=datetime.fromtimestamp(timestamp))

            content = 'Получаем криптовалюту, нужно немного подождать ⏳'

            await message.answer(content)

            time.sleep(await waiting_time())

            generated_crypto = await btc(user[4])

            if user[0] is None:
                await put_user(message.from_user.id, btc_balance=generated_crypto)
            else:
                await put_user(message.from_user.id, btc_balance=user[0] + generated_crypto)

            content = f'Вы получили {generated_crypto} ₿'

            await message.answer(content)
    except Exception as e:
        print(f'Play error: {e}')