import asyncio

from aiogram import Bot
from loguru import logger

from pkg.logging import Logger
from src.bot.bot import TgBot
from src.bot.keyboards.keyboards import Keyboard
from src.bot.lexicon.lexicon import Lexicon
from src.bot.routers.routers import routers
from src.config import Config
from src.services.calculate.bitinfocharts import BitinfochartsProfitability
from src.services.calculator import Calculator
from src.services.course_getter import CurrentCoursesGetter
from src.services.excel_provider import ExcelProvider
from src.storage.db.connect import DBConnect
from src.storage.redis.db_redis import RedisDatabase
from src.storage.storage import Storage


async def main() -> None:
    cfg = Config()

    log = Logger(
        log_level=cfg.log_level,
        log_dir_name=cfg.paths.log_dir_name,
        info_log_path=cfg.paths.info_log_path,
        debug_log_path=cfg.paths.debug_log_path,
    )
    log.setup_logger()
    logger.info("setup logger")
    logger.debug("debug is ON")

    bot = Bot(token=cfg.bot.token)

    storage = Storage(
        db=DBConnect(cfg.db.build_connection_str),
        redis=RedisDatabase(cfg),
    )

    lexicon = Lexicon()

    profit = BitinfochartsProfitability(storage.db)
    calc = Calculator(lexicon, cfg)

    course_getter = CurrentCoursesGetter(storage.redis)

    exel_provider = ExcelProvider()

    tg_bot = TgBot(
        bot=bot,
        storage=storage,
        lexicon=lexicon,
        profit=profit,
        calc=calc,
        course_getter=course_getter,
        exel_provider=exel_provider,
    )
    kb = Keyboard(lexicon.kb_name, cfg, calc)
    tg_bot.set_routers(routers)
    tg_bot.set_cfg(cfg)
    tg_bot.set_keyboards(kb)

    await asyncio.gather(
        tg_bot.run(),
        course_getter.run(),
    )


if __name__ == "__main__":
    asyncio.run(main())
