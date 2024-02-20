from loguru import logger
from sqlalchemy import select, Sequence, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.db.models import User


class UserRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def set(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        username: str,
        is_admin: bool,
    ) -> None:
        try:
            await self.session.merge(
                User(
                    user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    is_admin=is_admin,
                )
            )
            await self.session.commit()
            logger.info("User added to DB")
        except Exception as e:
            logger.error(f"Error while adding user to DB: {e}")

    async def get(self, user_id: int) -> User | None:
        stmt = select(User).where(User.user_id == user_id)
        return await self.session.scalar(stmt)

    async def get_all_by_limit_and_offset(
        self, offset: int, limit: int = 20
    ) -> list[User]:
        stmt = select(User).limit(limit).offset(offset * limit).where(User.is_blocked_by_user == False)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_quantity_all(self) -> int:
        stmt = select(func.count()).select_from(User).where(User.is_blocked_by_user == False)
        return await self.session.scalar(stmt)

    async def update(self, user: User) -> None:
        await self.session.merge(user)
        await self.session.commit()
