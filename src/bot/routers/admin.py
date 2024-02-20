import asyncio
from datetime import datetime

import aiofiles
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from src.bot.filters.filters import AdminFilter
from src.bot.keyboards.admin_menu import (
    AdminMenuData,
    AdminMenuActions,
    NewsletterMenuData,
    NewsletterMenuActions,
)
from src.bot.keyboards.keyboards import Keyboard
from src.bot.keyboards.main_menu import MainMenuData, MainMenuActions
from src.bot.lexicon.lexicon import Lexicon
from src.bot.states.admin_state import NewsletterState
from src.bot.utils.loop import send_messages_async
from src.services.excel_provider import ExcelProvider
from src.storage.db.db import Database
from src.storage.db.models import User

router = Router()


@router.callback_query(
    MainMenuData.filter(F.action == MainMenuActions.admin_menu), AdminFilter()
)
@router.callback_query(
    NewsletterMenuData.filter(F.action == NewsletterMenuActions.back), AdminFilter()
)
@router.callback_query(
    AdminMenuData.filter(F.action == AdminMenuActions.back), AdminFilter()
)
async def admin_menu(
    callback: CallbackQuery,
    kb: Keyboard,
    lexicon: Lexicon,
    state: FSMContext,
):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        text=lexicon.send.on_admin_menu,
        reply_markup=kb.admin_menu_kb.on_admin_menu_kb(),
    )


@router.callback_query(
    AdminMenuData.filter(F.action == AdminMenuActions.products_provider), AdminFilter()
)
async def products_provider(
    callback: CallbackQuery,
    kb: Keyboard,
    lexicon: Lexicon,
    excel: ExcelProvider,
    db: Database,
):
    await callback.answer()
    file_name = "products.xlsx"
    products = await db.product.get_all()
    if len(products) == 0:
        await excel.create(file_name)
    else:
        await excel.create(file_name, products)

    await callback.message.delete()
    await callback.message.answer_document(document=FSInputFile(file_name))
    await excel.delete(file_name)
    await callback.message.answer(
        text=lexicon.send.on_products_provider,
        reply_markup=kb.admin_menu_kb.on_products_provider_kb(),
    )


@router.callback_query(
    AdminMenuData.filter(F.action == AdminMenuActions.products_set_menu), AdminFilter()
)
async def products_set_menu(
    callback: CallbackQuery,
    kb: Keyboard,
    lexicon: Lexicon,
    state: FSMContext,
):
    await callback.answer()
    msg = await callback.message.edit_text(
        text=lexicon.send.on_products_set,
        reply_markup=kb.admin_menu_kb.cancel_kb(action=AdminMenuActions.back),
    )
    await state.set_state(NewsletterState.products_set)
    await state.update_data(msg_id_to_remove_mp=msg.message_id)


@router.message(F.document, NewsletterState.products_set, AdminFilter())
async def products_set(
    message: Message,
    db: Database,
    kb: Keyboard,
    lexicon: Lexicon,
    state: FSMContext,
    excel: ExcelProvider,
    bot: Bot,
):
    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    data = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=data["msg_id_to_remove_mp"]
    )

    if not file_info.file_path.endswith(".xlsx"):
        msg = await message.answer(
            text=lexicon.send.on_products_set_err,
            reply_markup=kb.admin_menu_kb.cancel_kb(action=AdminMenuActions.back),
        )
        await state.update_data(msg_id_to_remove_mp=msg.message_id)
        return

    file_path_tg = file_info.file_path
    downloaded_file = await bot.download_file(file_path_tg)
    file_path = "products_update.xlsx"
    async with aiofiles.open(file_path, "wb") as new_file:
        await new_file.write(downloaded_file.read())

    products = await excel.parse(file_path)
    if isinstance(products, str):
        msg = await message.answer(
            text=products,
            reply_markup=kb.admin_menu_kb.cancel_kb(action=AdminMenuActions.back),
        )
        await state.update_data(msg_id_to_remove_mp=msg.message_id)
        return

    if products is None:
        msg = await message.answer(
            text=lexicon.send.on_products_set_err,
            reply_markup=kb.admin_menu_kb.cancel_kb(action=AdminMenuActions.back),
        )
        await state.update_data(msg_id_to_remove_mp=msg.message_id)
        return

    await db.product.delete_all()
    for product in products:
        await db.product.set(
            category=product.category,
            name=product.name,
            terahesh=product.terahesh,
            consumption=product.consumption,
            price=product.price,
            algorithm=product.algorithm,
        )
    await excel.delete(file_path)
    await state.clear()
    await message.answer(text=lexicon.send.on_products_set_success)
    await message.answer(
        text=lexicon.send.on_admin_menu,
        reply_markup=kb.admin_menu_kb.on_admin_menu_kb(),
    )


@router.message(~F.document, NewsletterState.products_set, AdminFilter())
async def products_set_err(
    message: Message, lexicon: Lexicon, kb: Keyboard, state: FSMContext, bot: Bot
):
    data = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=data["msg_id_to_remove_mp"]
    )
    msg = await message.answer(
        text=lexicon.send.on_products_set_err,
        reply_markup=kb.admin_menu_kb.cancel_kb(action=AdminMenuActions.back),
    )
    await state.update_data(msg_id_to_remove_mp=msg.message_id)


@router.callback_query(
    AdminMenuData.filter(F.action == AdminMenuActions.user_menu), AdminFilter()
)
async def user_menu(
    callback: CallbackQuery,
    user: User,
    kb: Keyboard,
    lexicon: Lexicon,
):
    await callback.answer()
    await callback.message.edit_text(
        text=lexicon.send.on_user_menu.format(user.price_for_electricity),
        reply_markup=kb.main_menu_kb.on_main_menu_mp(
            user.price_for_electricity, user.is_admin
        ),
        parse_mode="HTML",
    )


@router.callback_query(
    AdminMenuData.filter(F.action == AdminMenuActions.newsletter), AdminFilter()
)
@router.callback_query(
    NewsletterMenuData.filter(F.action == NewsletterMenuActions.cancel), AdminFilter()
)
async def newsletter_menu(
    callback: CallbackQuery,
    kb: Keyboard,
    lexicon: Lexicon,
):
    await callback.message.edit_text(
        lexicon.send.on_newsletter,
        reply_markup=kb.admin_menu_kb.on_newsletter_kb(is_end_newsletter=False),
    )


@router.callback_query(
    NewsletterMenuData.filter(F.action == NewsletterMenuActions.yes),
    AdminFilter(),
)
async def newsletter_yes(
    callback: CallbackQuery,
    kb: Keyboard,
    lexicon: Lexicon,
    state: FSMContext,
):
    msg = await callback.message.edit_text(
        lexicon.send.on_newsletter_yes,
        reply_markup=kb.admin_menu_kb.cancel_kb(),
    )
    await state.set_state(NewsletterState.photo_or_video)
    await state.update_data(msg_id_to_remove_mp=msg.message_id)


@router.message(F.photo, NewsletterState.photo_or_video, AdminFilter())
@router.message(F.video, NewsletterState.photo_or_video, AdminFilter())
async def newsletter_photo_or_video(
    message: Message, bot: Bot, state: FSMContext, kb: Keyboard, lexicon: Lexicon
):
    data = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.from_user.id, message_id=data.get("msg_id_to_remove_mp")
    )
    if message.video:
        await state.update_data(media=message.video.file_id + "video")
    else:
        await state.update_data(media=message.photo[-1].file_id)
    msg = await message.answer(
        lexicon.send.on_newsletter_no_or_before_yes,
        reply_markup=kb.admin_menu_kb.cancel_kb(),
    )
    await state.update_data(msg_id_to_remove_mp=msg.message_id)
    await state.set_state(NewsletterState.text)


@router.message(~F.photo, NewsletterState.photo_or_video, AdminFilter())
@router.message(~F.video, NewsletterState.photo_or_video, AdminFilter())
async def newsletter_photo_or_video_bad(
    message: Message, bot: Bot, state: FSMContext, kb: Keyboard, lexicon: Lexicon
):
    data = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.from_user.id, message_id=data.get("msg_id_to_remove_mp")
    )
    msg = await message.answer(
        lexicon.send.on_newsletter_bad_video_photo,
        reply_markup=kb.admin_menu_kb.cancel_kb(),
    )
    await state.update_data(msg_id_to_remove_mp=msg.message_id)


@router.callback_query(
    NewsletterMenuData.filter(F.action == NewsletterMenuActions.no), AdminFilter()
)
async def newsletter_no(
    callback: CallbackQuery,
    kb: Keyboard,
    lexicon: Lexicon,
    state: FSMContext,
):
    msg = await callback.message.edit_text(
        lexicon.send.on_newsletter_no_or_before_yes,
        reply_markup=kb.admin_menu_kb.cancel_kb(),
    )
    await state.update_data(msg_id_to_remove_mp=msg.message_id)
    await state.set_state(NewsletterState.text)


@router.message(NewsletterState.text, AdminFilter())
async def newsletter_text(
    message: Message,
    kb: Keyboard,
    lexicon: Lexicon,
    state: FSMContext,
    bot: Bot,
):
    data = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=data.get("msg_id_to_remove_mp")
    )

    await state.update_data(text=message.text)
    text_newsletter = message.text
    media_newsletter = data.get("media")
    if media_newsletter:
        if "video" in media_newsletter:
            media_newsletter = media_newsletter.replace("video", "")
            await bot.send_video(
                chat_id=message.chat.id,
                video=media_newsletter,
                caption=lexicon.send.on_newsletter_end.format(text_newsletter),
                reply_markup=kb.admin_menu_kb.on_newsletter_kb(is_end_newsletter=True),
            )
        else:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=media_newsletter,
                caption=lexicon.send.on_newsletter_end.format(text_newsletter),
                reply_markup=kb.admin_menu_kb.on_newsletter_kb(is_end_newsletter=True),
            )
    else:
        await message.answer(
            text=lexicon.send.on_newsletter_end.format(text_newsletter),
            reply_markup=kb.admin_menu_kb.on_newsletter_kb(is_end_newsletter=True),
        )

    await state.set_state(NewsletterState.end)


@router.callback_query(
    NewsletterState.end,
    NewsletterMenuData.filter(F.action == NewsletterMenuActions.yes_send),
    AdminFilter(),
)
async def newsletter_end_yes(
    callback: CallbackQuery,
    kb: Keyboard,
    lexicon: Lexicon,
    state: FSMContext,
    db: Database,
):
    data = await state.get_data()
    media = data.get("media")
    text = data.get("text")

    await state.clear()
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    time_now = datetime.now()
    quantity_users = await db.user.get_quantity_all()
    await callback.message.answer(
        lexicon.send.on_newsletter_start_quantity.format(quantity_users)
    )
    await callback.message.answer(
        lexicon.send.on_admin_menu, reply_markup=kb.admin_menu_kb.on_admin_menu_kb()
    )
    offset = 0
    count_sended_all = 0
    while True:
        users = await db.user.get_all_by_limit_and_offset(limit=20, offset=offset)
        if len(users) == 0:
            break

        count_sended_pack = await send_messages_async(
            users, callback.bot, db, media, text
        )
        count_sended_all += count_sended_pack
        await asyncio.sleep(1)
        offset += 1

    time_end = datetime.now()
    time_duration = time_end - time_now
    await callback.message.answer(
        lexicon.send.on_newsletter_end_quantity.format(
            time_duration.seconds, count_sended_all, quantity_users
        )
    )
    await callback.message.answer(
        lexicon.send.on_admin_menu, reply_markup=kb.admin_menu_kb.on_admin_menu_kb()
    )


@router.callback_query(
    NewsletterState.end,
    NewsletterMenuData.filter(F.action == NewsletterMenuActions.no_send),
    AdminFilter(),
)
async def newsletter_end_no(
    callback: CallbackQuery,
    kb: Keyboard,
    lexicon: Lexicon,
    state: FSMContext,
):
    await state.clear()
    await callback.answer("Отправка рассылки отменена.")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        text=lexicon.send.on_admin_menu,
        reply_markup=kb.admin_menu_kb.on_admin_menu_kb(),
    )
