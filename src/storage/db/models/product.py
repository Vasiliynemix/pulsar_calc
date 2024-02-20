from sqlalchemy.orm import mapped_column, Mapped

from src.storage.db.models.base import Base


class Product(Base):
    category: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    terahesh: Mapped[float] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    consumption: Mapped[float] = mapped_column(nullable=False)
    algorithm: Mapped[str] = mapped_column(nullable=True)
