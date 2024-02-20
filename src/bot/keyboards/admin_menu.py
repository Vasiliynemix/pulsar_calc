import os
from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.lexicon.lexicon import LexiconMsgKbName


class AdminMenuActions(IntEnum):
    newsletter = auto()
    products_provider = auto()
    products_set_menu = auto()
    user_menu = auto()
    back = auto()


class NewsletterMenuActions(IntEnum):
    yes = auto()
    no = auto()
    yes_send = auto()
    no_send = auto()
    back = auto()
    cancel = auto()


class AdminMenuData(CallbackData, prefix=os.path.basename(__file__).split(".")[0]):
    action: AdminMenuActions


class NewsletterMenuData(
    CallbackData, prefix=f"{os.path.basename(__file__).split('.')[0]}_newsletter"
):
    action: NewsletterMenuActions
    is_end_newsletter: bool | None = None


class AdminMenuKeyboard:
    def __init__(self, kb_name: LexiconMsgKbName) -> None:
        self._kb_name = kb_name

    def cancel_kb(self, action: AdminMenuActions | NewsletterMenuActions | None = None) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        if isinstance(action, AdminMenuActions):
            callback_data = AdminMenuData(action=action)
        else:
            callback_data = NewsletterMenuData(
                action=NewsletterMenuActions.cancel,
                is_end_newsletter=False,
            )
        builder.button(
            text=self._kb_name.cancel.inline,
            callback_data=callback_data.pack(),
        )
        builder.adjust(1)
        return builder.as_markup()

    def on_admin_menu_kb(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=self._kb_name.products_provider.inline,
            callback_data=AdminMenuData(action=AdminMenuActions.products_provider).pack(),
        )
        builder.button(
            text=self._kb_name.newsletter.inline,
            callback_data=AdminMenuData(action=AdminMenuActions.newsletter).pack(),
        )
        builder.button(
            text=self._kb_name.user_menu.inline,
            callback_data=AdminMenuData(action=AdminMenuActions.user_menu).pack(),
        )
        builder.adjust(1, 1, 1)
        return builder.as_markup()

    def on_newsletter_kb(self, is_end_newsletter: bool = False) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        action_yes = NewsletterMenuActions.yes
        action_no = NewsletterMenuActions.no
        if is_end_newsletter:
            action_yes = NewsletterMenuActions.yes_send
            action_no = NewsletterMenuActions.no_send
        builder.button(
            text=self._kb_name.yes.inline,
            callback_data=NewsletterMenuData(
                action=action_yes, is_end_newsletter=is_end_newsletter
            ).pack(),
        )
        builder.button(
            text=self._kb_name.no.inline,
            callback_data=NewsletterMenuData(
                action=action_no, is_end_newsletter=is_end_newsletter
            ).pack(),
        )
        if is_end_newsletter is False:
            builder.button(
                text=self._kb_name.back.inline,
                callback_data=NewsletterMenuData(
                    action=NewsletterMenuActions.back,
                    is_end_newsletter=is_end_newsletter,
                ).pack(),
            )
        builder.adjust(2, 1)
        return builder.as_markup()

    def on_products_provider_kb(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=self._kb_name.products_set_new.inline,
            callback_data=AdminMenuData(action=AdminMenuActions.products_set_menu).pack(),
        )
        builder.button(
            text=self._kb_name.back.inline,
            callback_data=AdminMenuData(action=AdminMenuActions.back).pack(),
        )
        builder.adjust(1)
        return builder.as_markup()
