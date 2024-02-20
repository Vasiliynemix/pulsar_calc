from loguru import logger
from sqlalchemy import select, Sequence, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.db.models import User, Product


class ProductRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def set(
        self,
        category: str,
        name: str,
        terahesh: float,
        price: float,
        consumption: float,
        algorithm: str,
    ) -> None:
        try:
            await self.session.merge(
                Product(
                    category=category,
                    name=name,
                    terahesh=terahesh,
                    price=price,
                    consumption=consumption,
                    algorithm=algorithm,
                )
            )
            await self.session.commit()
        except Exception as e:
            logger.error(f"Error while adding product to DB: {e}")

    async def get_all(self) -> list[Product]:
        stmt = select(Product)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_categories(self) -> list[str]:
        stmt = select(func.distinct(Product.category)).order_by(Product.category)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_all_by_category(
        self, category: str, offset: int, limit: int = 10
    ) -> tuple[list[Product], bool]:
        stmt = (
            select(Product)
            .where(Product.category == category)
            .limit(limit)
            .offset(offset * limit)
            .order_by(Product.terahesh)
        )
        result = await self.session.scalars(stmt)
        next_offset = offset + 1
        stmt = (
            select(Product)
            .where(Product.category == category)
            .limit(limit)
            .offset(next_offset * limit)
        )
        next_batch = await self.session.scalars(stmt)
        return list(result.all()), len(next_batch.all()) > 0

    async def get_product(
        self, name: str, terahesh: float, consumption: float
    ) -> Product | None:
        stmt = select(Product).where(
            Product.name == name,
            Product.terahesh == terahesh,
            Product.consumption == consumption,
        )
        return await self.session.scalar(stmt)

    async def delete_all(self) -> None:
        stmt = delete(Product)
        await self.session.execute(stmt)
        await self.session.commit()
