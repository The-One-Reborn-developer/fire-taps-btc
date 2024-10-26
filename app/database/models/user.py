from sqlalchemy import BigInteger, String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[BigInteger] = mapped_column(BigInteger)
    phone: Mapped[String] = mapped_column(String, nullable=True)
    btc_balance: Mapped[float] = mapped_column(Float, nullable=True)
    referrals_amount: Mapped[int] = mapped_column(Integer, nullable=True)
    referral_code: Mapped[String] = mapped_column(String, nullable=True)