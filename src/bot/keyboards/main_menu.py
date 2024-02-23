import os
from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.lexicon.lexicon import LexiconMsgKbName
from src.config import Config
from src.storage.db.models import Product


class MainMenuActions(IntEnum):
    calculator = auto()
    price_setter = auto()
    cancel = auto()
    admin_menu = auto()
    back_to_main_menu = auto()
    back_to_categories = auto()
    back_to_main_menu_new_msg = auto()
    no_in_db = auto()


class MainMenuData(CallbackData, prefix=os.path.basename(__file__).split(".")[0]):
    action: MainMenuActions


class CategoriesData(CallbackData, prefix=f"c_m_m"):
    category: str
    offset: int


class AlgorithmData(CallbackData, prefix=f"a_m_m"):
    algorithm: str | None


class ProductsData(CallbackData, prefix=f"p_m_m"):
    name: str
    terahesh: float
    consumption: float
    offset: int


class MainMenuKeyboard:
    def __init__(self, kb_name: LexiconMsgKbName, cfg: Config) -> None:
        self._kb_name = kb_name
        self._cfg = cfg

    def on_main_menu_mp(
        self, price_for_electricity: float | None, is_admin: bool = False
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=self._kb_name.calculator.inline,
            callback_data=MainMenuData(action=MainMenuActions.calculator).pack(),
        )
        if price_for_electricity is not None:
            builder.button(
                text=self._kb_name.price_setter.inline,
                callback_data=MainMenuData(action=MainMenuActions.price_setter).pack(),
            )
        if is_admin:
            builder.button(
                text=self._kb_name.admin_menu.inline,
                callback_data=MainMenuData(action=MainMenuActions.admin_menu).pack(),
            )
        builder.adjust(1, 1, 1)
        return builder.as_markup()

    def cancel_mp(self):
        builder = InlineKeyboardBuilder()
        builder.button(
            text=self._kb_name.cancel.inline,
            callback_data=MainMenuData(action=MainMenuActions.cancel).pack(),
        )
        builder.adjust(1)
        return builder.as_markup()

    def categories_mp(self, categories: list[str], offset: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        if len(categories) != 0:
            for category in categories:
                builder.button(
                    text=f"🗂️{category}",
                    callback_data=CategoriesData(
                        category=category, offset=offset
                    ).pack(),
                )
        else:
            builder.button(
                text=self._kb_name.no_category_in_db.inline,
                callback_data=MainMenuData(action=MainMenuActions.no_in_db).pack(),
            )

        builder.button(
            text=self._kb_name.algorithm.inline,
            callback_data=AlgorithmData(algorithm="start_algorithm").pack(),
        )
        builder.button(
            text=self._kb_name.back.inline,
            callback_data=MainMenuData(action=MainMenuActions.back_to_main_menu).pack(),
        )
        builder.adjust(1)
        return builder.as_markup()

    def algorithm_mp(self, algorithms: list[str]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        if len(algorithms) != 0:
            for algorithm in algorithms:
                builder.button(
                    text=f"🔍{algorithm}",
                    callback_data=AlgorithmData(algorithm=algorithm).pack(),
                )
        else:
            builder.button(
                text=self._kb_name.no_algorithm_in_db.inline,
                callback_data=MainMenuData(action=MainMenuActions.no_in_db).pack(),
            )
        builder.button(
            text=self._kb_name.back.inline,
            callback_data=MainMenuData(
                action=MainMenuActions.back_to_categories
            ).pack(),
        )
        builder.adjust(1)
        return builder.as_markup()

    def products_mp(
        self, products: list[Product], offset: int, is_not_last_page: bool
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        if len(products) != 0:
            for product in products:
                terahesh = product.terahesh
                if terahesh.is_integer():
                    terahesh = int(terahesh)
                consumption = product.consumption
                if consumption.is_integer():
                    consumption = int(consumption)
                text = f"⛏️{product.name} {terahesh} Th {consumption} Вт"
                ikb_product = InlineKeyboardButton(
                    text=text,
                    callback_data=ProductsData(
                        name=product.name,
                        terahesh=product.terahesh,
                        consumption=product.consumption,
                        offset=offset,
                    ).pack(),
                )
                builder.row(ikb_product)

        ikb_prev = InlineKeyboardButton(
            text=self._kb_name.prev.inline,
            callback_data=CategoriesData(
                category=products[0].category,
                offset=offset - 1,
            ).pack(),
        )
        ikb_next = InlineKeyboardButton(
            text=self._kb_name.next.inline,
            callback_data=CategoriesData(
                category=products[0].category,
                offset=offset + 1,
            ).pack(),
        )
        if len(products) == 10:
            if offset == 0:
                builder.row(ikb_next)
            elif offset > 0:
                if is_not_last_page:
                    builder.row(ikb_prev, ikb_next)
                else:
                    builder.row(ikb_prev)
        else:
            if offset != 0:
                builder.row(ikb_prev)

        ikb_back = InlineKeyboardButton(
            text=self._kb_name.back.inline,
            callback_data=MainMenuData(
                action=MainMenuActions.back_to_categories
            ).pack(),
        )
        builder.row(ikb_back)
        return builder.as_markup()

    def back_to_main_menu_mp(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=self._kb_name.back_to_main_menu.inline,
            callback_data=MainMenuData(
                action=MainMenuActions.back_to_main_menu_new_msg
            ).pack(),
        )
        builder.adjust(1)
        return builder.as_markup()

    def chat_manager_mp(self, is_remove_back_to_main_menu_mp: bool) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=self._kb_name.chat_to_manager.inline,
            url=f"https://t.me/{self._cfg.manager_username}",
        )
        if not is_remove_back_to_main_menu_mp:
            builder.button(
                text=self._kb_name.back_to_main_menu.inline,
                callback_data=MainMenuData(
                    action=MainMenuActions.back_to_main_menu_new_msg
                ).pack(),
            )
        builder.adjust(1)
        return builder.as_markup()
