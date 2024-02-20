from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from src.storage.db.models.base import Base


class User(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    price_for_electricity: Mapped[float] = mapped_column(nullable=True)

    is_admin: Mapped[bool] = mapped_column(nullable=True, default=False)
    is_blocked_by_user: Mapped[bool] = mapped_column(nullable=True, default=False)
