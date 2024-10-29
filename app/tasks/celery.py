import celery
import logging

from app.database.models.user import User

from app.database.queues.create_tables import create_tables
from app.database.queues.get_user_by_id import get_user_by_id
from app.database.queues.get_user_by_play_referral import get_user_by_play_referral
from app.database.queues.get_user_by_registration_referral import get_user_by_registration_referral
from app.database.queues.post_user import post_user
from app.database.queues.put_user import put_user

from app.bot.convert_btc_to_usdt import convert_btc_to_usdt
from app.bot.create_check import create_check
from app.bot.get_balance import get_balance
from app.bot.get_btc_rate import get_btc_rate


app = celery.Celery('tasks', broker='redis://redis:6379/0')


app.conf.update(
    task_routes = {
        'app.tasks.celery.*': {'queue': 'all_queues'},
    },
    broker_connection_retry_on_startup = True,
    result_backend = 'redis://redis:6379/0',
)


@app.task
def create_tables_task() -> None:
    logging.info('Creating tables...')
    create_tables()
    logging.info('Tables created.')


@app.task
def get_user_by_id_task(telegram_id: int) -> User | None:
    logging.info(f'Getting user by ID: {telegram_id}')
    result = get_user_by_id(telegram_id)

    if result:
        logging.info(f'User by ID: {telegram_id} got.')
        return result
    else:
        logging.info(f'User by ID: {telegram_id} not found.')
        return None
    logging.info(f'User by ID: {telegram_id} got.')


@app.task
def get_user_by_play_referral_task(telegram_id: int) -> bool:
    logging.info(f'Getting user by play referral: {telegram_id}')
    result = get_user_by_play_referral(telegram_id)

    if result:
        logging.info(f'User by play referral: {telegram_id} got.')
        return True
    else:
        logging.info(f'User by play referral: {telegram_id} not found.')
        return False


@app.task
def get_user_by_registration_referral_task(referral_code: str) -> bool:
    logging.info(f'Getting user by registration referral: {referral_code}')
    result = get_user_by_registration_referral(referral_code)

    if result:
        logging.info(f'User by registration referral: {referral_code} got.')
        return True
    else:
        logging.info(f'User by registration referral: {referral_code} not found.')
        return False


@app.task
def post_user_task(user_id: int) -> None:
    logging.info(f'Posting user: {user_id}')
    post_user(user_id)
    logging.info(f'User: {user_id} posted.')


@app.task
def put_user_task(telegram_id: int, **kwargs) -> None:
    logging.info(f'Putting user: {telegram_id}')
    put_user(telegram_id, **kwargs)
    logging.info(f'User: {telegram_id} put.')


@app.task
def convert_btc_to_usdt_task(btc: float) -> float:
    logging.info('Converting BTC to USDT...')
    result = convert_btc_to_usdt(btc)

    if result:
        logging.info('BTC to USDT converted.')
        return result
    else:
        logging.info('BTC to USDT conversion failed.')
        return None


@app.task
def create_check_task(amount: float) -> int | dict | None:
    logging.info('Creating check...')
    result = create_check(amount)

    if result:
        if result == 400:
            logging.info('Invalid amount.')
            return 400
        logging.info('Check created.')
        return {
            'check_id': result.check_id,
            'amount': result.amount,
            'asset': result.asset,
            'created_at': result.created_at,
            'bot_check_url': result.bot_check_url
        }
    else:
        logging.info('Check creation failed.')
        return None


@app.task
def get_balance_task() -> float:
    logging.info('Getting balance...')
    result = get_balance()

    if result:
        logging.info('Balance got.')
        return result
    else:
        logging.info('Balance not found.')
        return None


@app.task
def get_btc_rate_task() -> float:
    logging.info('Getting BTC rate...')
    result = get_btc_rate()

    if result:
        logging.info('BTC rate got.')
        return result
    else:
        logging.info('BTC rate not found.')
        return None