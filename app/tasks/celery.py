import celery
import logging

from app.database.models.user import User

from app.database.queries.create_tables import create_tables
from app.database.queries.get_user_by_id import get_user_by_id
from app.database.queries.get_user_by_play_referral import get_user_by_play_referral
from app.database.queries.get_user_by_registration_referral import get_user_by_registration_referral
from app.database.queries.post_user import post_user
from app.database.queries.put_user import put_user

from app.bot.convert_btc_to_usdt import convert_btc_to_usdt
from app.bot.create_check import create_check
from app.bot.get_balance import get_balance
from app.bot.get_btc_rate import get_btc_rate


app = celery.Celery('tasks', broker='redis://redis:6379/0')


app.conf.update(
    task_routes={
        'app.tasks.celery.*': {'queue': 'all_queues'},
    },
    broker_connection_retry_on_startup=True,
    result_backend='redis://redis:6379/0',
)


@app.task
def create_tables_task() -> None:
    """
    Creates all tables defined in the application's metadata.

    Utilizes the synchronous engine to establish a connection and runs an operation 
    to create all tables. In the event of an error during table creation, logs the 
    exception message.

    Returns:
        None
    """
    logging.info('Creating tables...')
    create_tables()
    logging.info('Tables created.')


@app.task
def get_user_by_id_task(telegram_id: int) -> User | None:
    """
    Retrieves a user from the database by their telegram_id.

    Args:
        telegram_id (int): The telegram_id of the user to fetch.

    Returns:
        User | None: The user from the database, or None if no user was found.
    """
    logging.info(f'Getting user by ID: {telegram_id}')
    result = get_user_by_id(telegram_id)

    if result:
        logging.info(f'User by ID: {telegram_id} got.')
        return result
    else:
        logging.info(f'User by ID: {telegram_id} not found.')
        return None


@app.task
def get_user_by_play_referral_task(telegram_id: int) -> bool:
    """
    Retrieves a user from the database by their telegram_id and checks if the user's play referral code matches the current play referral.

    Args:
        telegram_id (int): The telegram_id of the user to fetch.

    Returns:
        bool: True if the user's play referral code matches the current play referral, False otherwise.
    """
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
    """
    Retrieves a user from the database by their registration referral code and checks if the user's registration referral code matches the current registration referral.

    Args:
        referral_code (str): The registration referral code of the user to fetch.

    Returns:
        bool: True if the user's registration referral code matches the current registration referral, False otherwise.
    """
    logging.info(f'Getting user by registration referral: {referral_code}')
    result = get_user_by_registration_referral(referral_code)

    if result:
        logging.info(f'User by registration referral: {referral_code} got.')
        return True
    else:
        logging.info(f'User by registration referral: {
                     referral_code} not found.')
        return False


@app.task
def post_user_task(user_id: int) -> None:
    """
    Creates a new user in the database if the user does not already exist.

    Args:
        user_id (int): The telegram_id of the user to create.

    Returns:
        None
    """
    logging.info(f'Posting user: {user_id}')
    post_user(user_id)
    logging.info(f'User: {user_id} posted.')


@app.task
def put_user_task(telegram_id: int, **kwargs) -> None:
    """
    Updates the user with the given telegram_id in the database with the given key-value arguments.

    Args:
        telegram_id (int): The telegram_id of the user to update.
        **kwargs: The key-value arguments to update the user with.

    Returns:
        None
    """
    logging.info(f'Putting user: {telegram_id}')
    put_user(telegram_id, **kwargs)
    logging.info(f'User: {telegram_id} put.')


@app.task
def convert_btc_to_usdt_task(btc: float) -> float:
    """
    Converts the given amount of Bitcoin to USDT.

    Args:
        btc (float): The amount of Bitcoin to convert.

    Returns:
        float | None: The converted amount of USDT or None if conversion fails.
    """
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
    """
    Creates a check for the specified amount of USDT using the crypto bot.

    Args:
        amount (float): The amount of USDT to create the check for.

    Returns:
        int | dict | None: A Check object if successful, or 400 if there is a validation error with the input amount, or None if the check creation failed.
    """
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
    """
    Gets the current balance of the CryptoBot account in USDT.

    Returns:
        float: The current balance of the CryptoBot account in USDT.

    Raises:
        Exception: If there is an error getting the balance.
    """
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
    """
    Gets the current rate of 1 BTC in RUB from the CryptoPay Bot.

    Returns:
        float: The current rate of 1 BTC in RUB.

    Raises:
        Exception: If there is an error getting the rate.
    """
    logging.info('Getting BTC rate...')
    result = get_btc_rate()

    if result:
        logging.info('BTC rate got.')
        return result
    else:
        logging.info('BTC rate not found.')
        return None
