from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.base import BaseStorage, BaseEventIsolation
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommand
from loguru import logger

from src.bot.keyboards.keyboards import Keyboard
from src.bot.lexicon.lexicon import Lexicon
from src.bot.middlewares.middlewares import TGBotMiddleware
from src.config import Config
from src.services.calculate.bitinfocharts import BitinfochartsProfitability
from src.services.calculator import Calculator
from src.services.course_getter import CurrentCoursesGetter
from src.services.excel_provider import ExcelProvider
from src.storage.storage import Storage


class TgBot:
    def __init__(
        self,
        bot: Bot,
        storage: Storage,
        lexicon: Lexicon,
        profit: BitinfochartsProfitability,
        calc: Calculator,
        course_getter: CurrentCoursesGetter,
        exel_provider: ExcelProvider,
    ) -> None:
        self.bot: Bot = bot
        self.storage: Storage = storage
        self.profit: BitinfochartsProfitability = profit
        self.calc: Calculator = calc
        self.course_getter = course_getter
        self.exel_provider = exel_provider
        self.routers: tuple[Router] | None = None
        self.cfg: Config | None = None
        self.lexicon = lexicon
        self.keyboard = None

    def set_routers(self, routers: tuple[Router]) -> None:
        self.routers = routers

    def set_cfg(self, cfg: Config) -> None:
        self.cfg = cfg

    def set_keyboards(self, keyboard: Keyboard) -> None:
        self.keyboard = keyboard

    async def run(self) -> None:
        try:
            storage = await self.storage.redis.get_redis_storage()
            # storage = MemoryStorage()
            dp = self.__get_dispatcher(storage=storage)

            try:
                logger.info(f"START Bot... {await self.bot.get_my_name()}")
                await self.__set_main_menu()
            except Exception as e:
                logger.error(e)

            # await self.__update_base_if_needed()

            await dp.start_polling(
                self.bot,
                allowed_updates=dp.resolve_used_update_types(),
                db=None,
                redis=self.storage.redis,
                user=None,
                cfg=self.cfg,
                lexicon=self.lexicon,
                kb=self.keyboard,
                profit=self.profit,
                calc=self.calc,
                course_getter=self.course_getter,
                excel=self.exel_provider,
            )
        except Exception as e:
            logger.error(e)
        finally:
            await self.bot.session.close()
            logger.info("FINISH Bot...")

    async def __set_main_menu(self) -> None:
        main_menu_commands = [
            BotCommand(command=command, description=description)
            for command, description in self.lexicon.COMMANDS.items()
        ]
        await self.bot.set_my_commands(main_menu_commands)

    def __get_dispatcher(
        self,
        storage: BaseStorage | None = MemoryStorage(),
        fsm_strategy: FSMStrategy | None = FSMStrategy.CHAT,
        event_isolation: BaseEventIsolation | None = None,
    ) -> Dispatcher:
        dp = Dispatcher(
            storage=storage,
            fsm_strategy=fsm_strategy,
            events_isolation=event_isolation,
        )

        dp.include_routers(*self.routers)

        tg_mw = TGBotMiddleware(self.storage)
        tg_mw.setup(dp)

        return dp
