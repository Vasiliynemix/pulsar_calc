import asyncio
from collections import Counter

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from loguru import logger

from src.storage.db.db import Database
from src.storage.db.models import User


async def send_messages_async(
    users: list[User], bot: Bot, db: Database, media: str | None, text: str
) -> int:
    tasks = []
    count_sended = Counter()
    for user in users:
        task = asyncio.create_task(send_msg(user, text, media, bot, db, count_sended))
        tasks.append(task)

    await asyncio.gather(*tasks)
    return sum(count_sended.values())


async def send_msg(
    user: User, text: str, media: str | None, bot: Bot, db: Database, count_sended
) -> None:
    try:
        if media is not None:
            if "video" in media:
                media = media.replace("video", "")
                await bot.send_video(chat_id=user.user_id, video=media, caption=text)
            else:
                await bot.send_photo(chat_id=user.user_id, photo=media, caption=text)
        else:
            await bot.send_message(chat_id=user.user_id, text=text)
        count_sended["success"] += 1
    except TelegramRetryAfter as e:
        logger.warning(f"Retry newsletter after {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
    except TelegramForbiddenError:
        user.is_blocked_by_user = True
        await db.user.update(user)
    except Exception as e:
        logger.error(e)
