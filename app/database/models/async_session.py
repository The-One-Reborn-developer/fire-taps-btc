from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.async_engine import async_engine


async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)