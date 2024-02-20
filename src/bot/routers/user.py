from datetime import datetime, timezone, timedelta

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from src.bot.keyboards.keyboards import Keyboard
from src.bot.keyboards.main_menu import (
    MainMenuData,
    MainMenuActions,
    CategoriesData,
    ProductsData,
    AlgorithmData,
)
from src.bot.lexicon.lexicon import Lexicon
from src.bot.states.user_state import UserSetPriceForElectricityState, AlgorithmState
from src.config import Config
from src.services.calculate.bitinfocharts import BitinfochartsProfitability
from src.services.calculator import Calculator
from src.storage.db.db import Database
from src.storage.db.models import User, Product
from src.storage.redis.db_redis import RedisDatabase

router = Router()


@router.message(Command("rate"))
async def course_command(message: Message, redis: RedisDatabase):
    current_course = await redis.get_course()
    if current_course is None:
        return
    await message.answer(f"1 usdt = {current_course} ₽")


@router.callback_query(
    MainMenuData.filter(F.action == MainMenuActions.cancel),
    UserSetPriceForElectricityState.price,
)
async def on_cancel_click(
    callback: CallbackQuery,
    state: FSMContext,
    lexicon: Lexicon,
    kb: Keyboard,
    user: User,
):
    await state.clear()
    text = lexicon.send.on_main_menu.format(
        user.price_for_electricity
        if user.price_for_electricity
        else "\nНе установлена, сперва установите цену."
    )
    if user.price_for_electricity is None:
        text = text.replace("₽.", "").strip()
    await callback.message.edit_text(
        text=text,
        reply_markup=kb.main_menu_kb.on_main_menu_mp(
            user.price_for_electricity, user.is_admin
        ),
        parse_mode="HTML",
    )


@router.callback_query(
    MainMenuData.filter(F.action == MainMenuActions.back_to_main_menu),
)
async def back_to_main_menu(
    callback: CallbackQuery,
    user: User,
    lexicon: Lexicon,
    state: FSMContext,
    kb: Keyboard,
):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(
        text=lexicon.send.on_main_menu.format(user.price_for_electricity),
        reply_markup=kb.main_menu_kb.on_main_menu_mp(
            user.price_for_electricity, user.is_admin
        ),
        parse_mode="HTML",
    )


@router.callback_query(MainMenuData.filter(F.action == MainMenuActions.calculator))
@router.callback_query(
    MainMenuData.filter(F.action == MainMenuActions.back_to_categories)
)
async def on_calculator_click(
    callback: CallbackQuery,
    user: User,
    lexicon: Lexicon,
    state: FSMContext,
    kb: Keyboard,
    db: Database,
):
    await callback.answer()
    if user.price_for_electricity is None:
        await callback.message.answer(lexicon.send.on_calc_click_without_price)
        await state.set_state(UserSetPriceForElectricityState.price)
        await state.update_data(msg_id_to_remove_mp=callback.message.message_id)
        return

    categories = await db.product.get_categories()
    await callback.message.edit_text(
        text=lexicon.send.on_calc_click.format(user.price_for_electricity),
        reply_markup=kb.main_menu_kb.categories_mp(categories, 0),
    )


@router.callback_query(
    MainMenuData.filter(F.action == MainMenuActions.no_in_db),
)
async def no_category_in_db(callback: CallbackQuery):
    await callback.answer(cache_time=300)


@router.callback_query(
    CategoriesData.filter(),
)
async def on_category_click(
    callback: CallbackQuery,
    callback_data: CategoriesData,
    lexicon: Lexicon,
    kb: Keyboard,
    db: Database,
):
    await callback.answer()
    products, is_not_last_page = await db.product.get_all_by_category(
        callback_data.category, callback_data.offset
    )
    await callback.message.edit_text(
        text=lexicon.send.on_category_click,
        reply_markup=kb.main_menu_kb.products_mp(
            products, callback_data.offset, is_not_last_page
        ),
    )


@router.callback_query(ProductsData.filter())
async def on_product_click(
    callback: CallbackQuery,
    callback_data: ProductsData,
    lexicon: Lexicon,
    kb: Keyboard,
    db: Database,
    user: User,
    redis: RedisDatabase,
    profit: BitinfochartsProfitability,
    cfg: Config,
    bot: Bot,
    calc: Calculator,
):
    product = await db.product.get_product(
        callback_data.name, callback_data.terahesh, callback_data.consumption
    )
    if product is None:
        await callback.answer(
            text="Ошибка на сервере, попробуйте позже...",
            cache_time=30,
        )
        return

    mining_profitability_usdt = await profit.parse_mining_profitability_usdt()
    if mining_profitability_usdt is None:
        await callback.answer(
            text="Ошибка на сервере, попробуйте позже...",
            cache_time=30,
        )
        return

    course = await redis.get_course()
    caption = await calc.start_calculate_by_algorithm_and_get_text(
        algorithm="",
        mining_profitability_usdt=mining_profitability_usdt,
        product=product,
        course=course,
        price_for_electricity=user.price_for_electricity,
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Начал расчет...")
    await callback.message.answer(
        text=caption,
        reply_markup=kb.main_menu_kb.back_to_main_menu_mp(),
        parse_mode="HTML",
    )


@router.callback_query(AlgorithmData.filter(F.algorithm == "start_algorithm"))
@router.callback_query(
    MainMenuData.filter(F.action == MainMenuActions.cancel),
    AlgorithmState.terahesh,
)
@router.callback_query(
    MainMenuData.filter(F.action == MainMenuActions.cancel),
    AlgorithmState.consumption,
)
async def on_algorithm_click(
    callback: CallbackQuery,
    lexicon: Lexicon,
    kb: Keyboard,
    calc: Calculator,
    state: FSMContext,
):
    await state.clear()
    await callback.message.edit_text(
        text=lexicon.send.on_algorithm_click,
        reply_markup=kb.main_menu_kb.algorithm_mp(calc.algorithms),
    )


@router.callback_query(AlgorithmData.filter())
async def on_one_algorithm_click(
    callback: CallbackQuery,
    callback_data: AlgorithmData,
    state: FSMContext,
    lexicon: Lexicon,
    kb: Keyboard,
):
    await state.set_state(AlgorithmState.terahesh)
    await state.update_data(algorithm=callback_data.algorithm)
    msg = await callback.message.edit_text(
        text=lexicon.send.on_one_algorithm,
        reply_markup=kb.main_menu_kb.cancel_mp(),
    )
    await state.update_data(msg_id_to_remove_mp=msg.message_id)


@router.message(AlgorithmState.terahesh)
async def on_algorithm_terahesh(
    message: Message,
    state: FSMContext,
    lexicon: Lexicon,
    kb: Keyboard,
    bot: Bot,
):
    data = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=data.get("msg_id_to_remove_mp"),
        reply_markup=None,
    )
    try:
        float(message.text)
    except ValueError:
        msg = await message.answer(
            text=lexicon.send.on_price_setter_err,
            reply_markup=kb.main_menu_kb.cancel_mp(),
        )
        await state.update_data(msg_id_to_remove_mp=msg.message_id)
        return

    await state.update_data(terahesh=float(message.text))
    msg = await message.answer(
        text=lexicon.send.on_algorithm_consumption_set,
        reply_markup=kb.main_menu_kb.cancel_mp(),
    )
    await state.update_data(msg_id_to_remove_mp=msg.message_id)
    await state.set_state(AlgorithmState.consumption)


@router.message(AlgorithmState.consumption)
async def on_algorithm_consumption(
    message: Message,
    state: FSMContext,
    lexicon: Lexicon,
    kb: Keyboard,
    bot: Bot,
    calc: Calculator,
    cfg: Config,
    profit: BitinfochartsProfitability,
    redis: RedisDatabase,
    user: User,
):
    data = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=data.get("msg_id_to_remove_mp"),
        reply_markup=None,
    )
    try:
        float(message.text)
    except ValueError:
        msg = await message.answer(
            text=lexicon.send.on_price_setter_err,
            reply_markup=kb.main_menu_kb.cancel_mp(),
        )
        await state.update_data(msg_id_to_remove_mp=msg.message_id)
        return

    mining_profitability_usdt = await profit.parse_mining_profitability_usdt()
    if mining_profitability_usdt is None:
        await message.answer(
            text="Ошибка на сервере, попробуйте позже...",
            cache_time=30,
        )
        return

    course = await redis.get_course()
    consumption = float(message.text)
    product = Product(
        name=data.get("algorithm"),
        consumption=consumption,
        terahesh=data.get("terahesh"),
        price=0,
    )
    caption = await calc.start_calculate_by_algorithm_and_get_text(
        algorithm=data.get("algorithm"),
        mining_profitability_usdt=mining_profitability_usdt,
        product=product,
        course=course,
        price_for_electricity=user.price_for_electricity,
    )
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=FSInputFile(cfg.paths.calc_image_path),
        caption=caption,
        reply_markup=kb.main_menu_kb.back_to_main_menu_mp(),
        parse_mode="HTML",
    )
    await state.clear()


@router.callback_query(
    MainMenuData.filter(F.action == MainMenuActions.back_to_main_menu_new_msg)
)
async def on_back_to_main_menu_new_msg_click(
    callback: CallbackQuery,
    user: User,
    lexicon: Lexicon,
    kb: Keyboard,
):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        text=lexicon.send.on_main_menu.format(user.price_for_electricity),
        reply_markup=kb.main_menu_kb.on_main_menu_mp(
            user.price_for_electricity, user.is_admin
        ),
        parse_mode="HTML",
    )


@router.callback_query(MainMenuData.filter(F.action == MainMenuActions.price_setter))
async def on_price_setter_click(
    callback: CallbackQuery,
    user: User,
    state: FSMContext,
    lexicon: Lexicon,
    kb: Keyboard,
):
    await callback.answer()
    msg = await callback.message.edit_text(
        text=lexicon.send.on_update_price_for_el.format(user.price_for_electricity),
        reply_markup=kb.main_menu_kb.cancel_mp(),
        parse_mode="HTML",
    )
    await state.set_state(UserSetPriceForElectricityState.price)
    await state.update_data(msg_id_to_remove_mp=msg.message_id)
    return


@router.message(UserSetPriceForElectricityState.price)
async def on_price_set(
    message: Message,
    state: FSMContext,
    db: Database,
    user: User,
    lexicon: Lexicon,
    kb: Keyboard,
    bot: Bot,
):
    data = await state.get_data()
    try:
        price_for_electricity = float(message.text.replace(",", "."))
    except ValueError:
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=data["msg_id_to_remove_mp"],
        )
        msg = await message.answer(
            text=lexicon.send.on_price_setter_err,
            reply_markup=kb.main_menu_kb.cancel_mp(),
        )
        await state.update_data(msg_id_to_remove_mp=msg.message_id)
        return

    user.price_for_electricity = price_for_electricity
    await db.user.update(user)
    await state.clear()

    await bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=data["msg_id_to_remove_mp"],
    )

    await message.answer(
        text=lexicon.send.on_main_menu.format(price_for_electricity),
        reply_markup=kb.main_menu_kb.on_main_menu_mp(
            user.price_for_electricity, user.is_admin
        ),
        parse_mode="HTML",
    )
