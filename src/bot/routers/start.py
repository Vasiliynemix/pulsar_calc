from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from src.bot.filters.filters import RegisterFilter
from src.bot.keyboards.keyboards import Keyboard
from src.bot.lexicon.lexicon import Lexicon
from src.config import Config
from src.storage.db.db import Database
from src.storage.db.models import User

router = Router()


@router.message(CommandStart(), RegisterFilter())
async def start_register(
    message: Message,
    lexicon: Lexicon,
    kb: Keyboard,
    state: FSMContext,
    db: Database,
) -> None:
    await state.clear()
    user = await db.user.get(message.from_user.id)
    await message.answer(
        lexicon.send.on_start_cmd_register,
        reply_markup=kb.main_menu_kb.on_main_menu_mp(
            user.price_for_electricity, user.is_admin
        ),
    )


@router.message(CommandStart())
async def start(
    message: Message,
    lexicon: Lexicon,
    kb: Keyboard,
    user: User,
    state: FSMContext,
    db: Database,
) -> None:
    await state.clear()
    if user.is_blocked_by_user:
        user.is_blocked_by_user = False
        await db.user.update(user)

    price_for_electricity_text = (
        f"\n\n<b>Установленная цена за 1 кВт/ч:</b> {user.price_for_electricity} ₽."
        if user.price_for_electricity
        else ""
    )
    await message.answer(
        text=lexicon.send.on_start_cmd.format(price_for_electricity_text),
        reply_markup=kb.main_menu_kb.on_main_menu_mp(
            user.price_for_electricity, user.is_admin
        ),
        parse_mode="HTML",
    )
