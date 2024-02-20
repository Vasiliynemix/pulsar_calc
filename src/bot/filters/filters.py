from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.lexicon.lexicon import Lexicon
from src.config import Config
from src.storage.db.db import Database
from src.storage.db.models import User


class RegisterFilter(BaseFilter):
    async def __call__(
        self, message: Message, db: Database, user: User, cfg: Config
    ) -> bool:
        if user is not None:
            return False

        is_admin = False
        if message.from_user.id in cfg.admins:
            is_admin = True

        await db.user.set(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            is_admin=is_admin,
        )
        return True


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, db: Database, user: User) -> bool:
        return user.is_admin


class MainMenuKBReplyFilter(BaseFilter):
    async def __call__(self, message: Message, lexicon: Lexicon) -> bool:
        return message.text == lexicon.kb_name.main_menu.reply
