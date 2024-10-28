from sqlalchemy import BigInteger, String, Float, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[BigInteger] = mapped_column(BigInteger)
    phone: Mapped[String] = mapped_column(String, nullable=True)
    btc_balance: Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
    referrals_amount: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    registration_referral_code: Mapped[String] = mapped_column(String, nullable=True)
    play_referral_code: Mapped[String] = mapped_column(String, nullable=True)
    last_played: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    number_of_plays: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    level: Mapped[int] = mapped_column(Integer, nullable=True, default=1)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=True)