import os

from sqlalchemy.ext.asyncio import create_async_engine

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


try:
    database_url = os.getenv('DATABASE_URL')
    async_engine = create_async_engine(database_url, echo=False)
except Exception as e:
    print(f'Error creating database engine: {e}')