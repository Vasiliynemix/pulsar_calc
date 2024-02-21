MAIN_MENU_KB = "🏠Главное меню"
CALCULATOR_KB = "🧮Калькулятор"
PRICE_SETTER_KB = "💡🔧Изменить цену за электроэнергию"
BACK_KB = "⬅️Назад"
BACK_TO_MAIN_MENU_KB = "🏠В главное меню"
CANCEL_KB = "❌Отмена"
YES_KB = "✅Да"
NO_KB = "❌Нет"

ALGORITHM_KB = "🔑Рассчитать по алгоритму"
NO_CATEGORY_IN_DB_KB = "❓Нет категорий"
NO_ALGORITHM_IN_DB_KB = "❓Нет алгоритмов"

PREV_KB = "⬅️"
NEXT_KB = "➡️"

ADMIN_PANEL_KB = "👮Админ панель"
USER_PANEL_KB = "👤Пользовательская панель"
NEWSLETTER_KB = "📧📤Рассылка"
PRODUCTS_PROVIDER_KB = "📋Список товаров"
PRODUCTS_SET_NEW_KB = "🔄Изменить/добавить товар"


class Lexicon:
    COMMANDS = {
        "/start": "Перезапустить бота",
        "/rate": "Текущий курс USDT",
    }

    LEXICON = {
        "msg_send": {
            "on_start_register": """Привет!👋 Я помогу тебе рассчитать доход с майнеров.

    ⚠️⚠️⚠️
    🛠️При первом нажатии на 🧮 Калькулятор нужно будет ввести стоимость розетки в рублях.

    💰Я запомню ее и в дальнейшем буду использовать в расчетах.

    🔄Значение можно будет изменить по кнопке, которая появится после ввода стоимости розетки.

    @pulsar_mining""",

            # "on_start_register": (
            #     "Привет!👋 Я помогу тебе рассчитать доход с майнеров.\n\n"
            #     "⚠️⚠️⚠️\n"
            #     "🛠️При первом нажатии на 🧮 Калькулятор нужно будет ввести стоимость розетки в рублях.\n\n"
            #     "💰Я запомню ее и в дальнейшем буду использовать в расчетах.\n\n"
            #     "🔄Значение можно будет изменить по кнопке, которая появится после ввода стоимости розетки.\n\n"
            #     "@pulsar_mining"
            # ),

            "on_start": "🏠Главное меню{}\n\n@pulsar_mining",
            "on_calc_click": "🔍Выбери категорию для расчета доходности.",
            "on_calc_click_without_price": "🛠️Для начала работы напиши мне стоимость твоей розетки в рублях.👇\n\n💡 Например: 3.5 или 2.44.",
            "on_update_price_for_el": "✨Напиши мне стоимость твоей розетки в рублях.\n\n💵 <b>Текущая стоимость:</b > {} ₽.",
            "on_price_setter_err": "⚠️Значение должно быть целым или вещественным числом.👇\n\n💡 Например: 3.5 или 2.44.",
            "on_main_menu_click": "🏠Главное меню\n\n<b>💡 Установленная цена за 1 кВт/ч:</b> {} ₽.\n\n@pulsar_mining",
            "on_admin_menu_click": ADMIN_PANEL_KB,
            "on_products_provider_click": (
                f"🔧Для добавления, удаления и изменения товаров, отредактируйте файл, что 🤖 бот отправил выше.👆\n\n"
                f"После того, как отредактируете файл:\n"
                f"🖲️Нажмите на кнопку {PRODUCTS_SET_NEW_KB} и отправьте отредактированный файл боту.👇\n\n"
                f"⚠️Все поля в файле должны быть заполнены.\n"
                f"⚠️Потребление в Вт/ч, Цена в usdt.\n"
            ),
            "on_products_set_click": (
                "Отправьте измененный файл списка товаров 🤖 боту.👇"
            ),
            "on_one_algorithm_click": "Введи количество Th/s(терахеш).👇",
            "on_products_set_err": "Отправьте документ в формате xlsx.👇",
            "on_products_set_err_value": (
                "⚠️Неверное значение.\n\n"
                "Хешрейт, Потребление и Цена должны быть целым или вещественным числом.\n"
                "Отправьте документ в формате xlsx.👇"
            ),
            "on_products_set_success": (
                "✅Товары были успешно обновлены и добавлены в базу."
            ),
            "on_newsletter_click": (
                f"Можно создать рассылку с 1 фото или видео.\n\n"
                f"Отправляем с медиа или нет?👇\n\n"
                f"В любой момент можно отменить создание рассылки нажав на кнопку {CANCEL_KB}."
            ),
            "on_newsletter_yes_click": (
                f"👌Отлично, отправь 1 фото или видео.👇\n\n"
                f"В любой момент можно отменить создание рассылки нажав на кнопку {CANCEL_KB}."
            ),
            "on_newsletter_bad_video_photo_send": ("⚠️Отправьте 1 фото или видео.👇\n"),
            "on_newsletter_no_click": (
                f"👌Отлично, отправь текст рассылки.👇\n\n"
                f"В любой момент можно отменить создание рассылки нажав на кнопку {CANCEL_KB}."
            ),
            "on_newsletter_create_end": "Текст рассылки:\n\n{}\n\nОтправляем?👇",
            "on_newsletter_start_quantity": (
                "🚀 Начал рассылать сообщения.\n\nКоличество пользователей для рассылки: {}"
            ),
            "on_newsletter_end_quantity": (
                "✅Закончил рассылать сообщения.\n\nЗатраченное время: {} с.\nКоличество отправленных сообщений: {}/{}"
            ),
            "on_algorithm_consumption_set": "Напиши мне потребление аппарата в Вт/ч.👇\n\n💡 Например: 3450 или 3500.",
            "on_user_menu_click": "🏠Главное меню\n\n<b>💡 Установленная цена за 1 кВт/ч:</b> {} ₽.\n\n@pulsar_mining",
            "on_category_click": "🔍Выберите товар для расчета доходности.",
            "on_algorithm_click": "🔍Выберите алгоритм для расчета доходности.",
            "algorithm_calculate": (
                "<b>Алгоритм: {name} {terahesh} Th.</b>\n"
                "<b>Потребление: {consumption} кВт/ч.</b>\n\n"
                "<b>Цена за 1 кВт/ч: {price_for_electricity} ₽.</b>\n"
                "<b>----------------------------------</b>\n"
                "<b>Расчет прибыли за день:</b>\n"
                "<b>Доход:</b> {profit_black_day} ₽.\n"
                "<b>Расход:</b> {cost_day} ₽.\n"
                "<b>Прибыль:</b> {profit_white_day} ₽.\n\n"
                "<b>Расчет прибыли за месяц:</b>\n"
                "<b>Доход:</b> {profit_black_moth} ₽.\n"
                "<b>Расход:</b> {cost_moth} ₽.\n"
                "<b>Прибыль:</b> {profit_white_moth} ₽.\n"
                "<b>----------------------------------</b>\n\n"
                "<b>Дата расчета: {time_now} (МСК).</b>\n\n"
                "<b>1 usdt = {course} ₽.</b>"
            ),
            "on_product_click": (
                "<b>Модель: {name} {terahesh} Th.</b>\n\n"
                "<b>Потребление: {consumption} кВт/ч.</b>\n"
                "<b>Стоимость: {price_rub} ₽ ({price_usdt} usdt).</b>\n\n"
                "<b>Цена за 1 кВт/ч: {price_for_electricity} ₽.</b>\n"
                "<b>----------------------------------</b>\n"
                "<b>Расчет прибыли за день:</b>\n"
                "<b>Доход:</b> {profit_black_day} ₽.\n"
                "<b>Расход:</b> {cost_day} ₽.\n"
                "<b>Прибыль:</b> {profit_white_day} ₽.\n\n"
                "<b>Расчет прибыли за месяц:</b>\n"
                "<b>Доход:</b> {profit_black_moth} ₽.\n"
                "<b>Расход:</b> {cost_moth} ₽.\n"
                "<b>Прибыль:</b> {profit_white_moth} ₽.\n"
                "<b>----------------------------------</b>\n"
                "<b>Срок окупаемости:</b> {term} мес.\n\n"
                "<b>Дата расчета: {time_now} (МСК).</b>\n\n"
                "<b>1 usdt = {course} ₽.</b>"
            ),
        },
        "msg_kb_name": {
            "cancel": {
                "reply": CANCEL_KB,
                "inline": CANCEL_KB,
            },
            "yes": {
                "reply": YES_KB,
                "inline": YES_KB,
            },
            "no": {
                "reply": NO_KB,
                "inline": NO_KB,
            },
            "main_manu": {
                "reply": MAIN_MENU_KB,
                "inline": MAIN_MENU_KB,
            },
            "price_setter": {
                "reply": PRICE_SETTER_KB,
                "inline": PRICE_SETTER_KB,
            },
            "calculator": {
                "reply": CALCULATOR_KB,
                "inline": CALCULATOR_KB,
            },
            "back": {
                "reply": BACK_KB,
                "inline": BACK_KB,
            },
            "back_to_main_menu": {
                "reply": BACK_TO_MAIN_MENU_KB,
                "inline": BACK_TO_MAIN_MENU_KB,
            },
            "admin_menu": {
                "reply": ADMIN_PANEL_KB,
                "inline": ADMIN_PANEL_KB,
            },
            "user_menu": {
                "reply": USER_PANEL_KB,
                "inline": USER_PANEL_KB,
            },
            "newsletter": {
                "reply": NEWSLETTER_KB,
                "inline": NEWSLETTER_KB,
            },
            "products_provider": {
                "reply": PRODUCTS_PROVIDER_KB,
                "inline": PRODUCTS_PROVIDER_KB,
            },
            "products_set_new": {
                "reply": PRODUCTS_SET_NEW_KB,
                "inline": PRODUCTS_SET_NEW_KB,
            },
            "prev": {
                "reply": PREV_KB,
                "inline": PREV_KB,
            },
            "next": {
                "reply": NEXT_KB,
                "inline": NEXT_KB,
            },
            "no_category_in_db": {
                "reply": NO_CATEGORY_IN_DB_KB,
                "inline": NO_CATEGORY_IN_DB_KB,
            },
            "no_algorithm_in_db": {
                "reply": NO_ALGORITHM_IN_DB_KB,
                "inline": NO_ALGORITHM_IN_DB_KB,
            },
            "algorithm": {
                "reply": ALGORITHM_KB,
                "inline": ALGORITHM_KB,
            },
        },
    }

    def __init__(self) -> None:
        self._lexicon = self.LEXICON
        self.cmd: LexiconCmdMsg = LexiconCmdMsg(self.COMMANDS)
        self.send: LexiconMsgSend = LexiconMsgSend(self._lexicon)
        self.kb_name: LexiconMsgKbName = LexiconMsgKbName(self._lexicon)


class LexiconCmdMsg:
    def __init__(self, commands: dict[str, str]) -> None:
        self._commands = commands
        self.start = "/start"


class LexiconMsgSend:
    def __init__(self, lexicon: dict[str, str | dict[str, str]]) -> None:
        self._lexicon = lexicon["msg_send"]
        self.on_start_cmd_register = self._lexicon["on_start_register"]
        self.on_start_cmd = self._lexicon["on_start"]
        self.on_main_menu = self._lexicon["on_main_menu_click"]
        self.on_calc_click_without_price = self._lexicon["on_calc_click_without_price"]
        self.on_calc_click = self._lexicon["on_calc_click"]
        self.on_price_setter_err = self._lexicon["on_price_setter_err"]
        self.on_update_price_for_el = self._lexicon["on_update_price_for_el"]

        self.on_category_click = self._lexicon["on_category_click"]
        self.on_algorithm_click = self._lexicon["on_algorithm_click"]

        self.on_product_click = self._lexicon["on_product_click"]
        self.algorithm_calculate = self._lexicon["algorithm_calculate"]

        self.on_admin_menu = self._lexicon["on_admin_menu_click"]
        self.on_newsletter = self._lexicon["on_newsletter_click"]
        self.on_products_provider = self._lexicon["on_products_provider_click"]
        self.on_products_set = self._lexicon["on_products_set_click"]
        self.on_products_set_err = self._lexicon["on_products_set_err"]
        self.on_products_set_err_value = self._lexicon["on_products_set_err_value"]
        self.on_products_set_success = self._lexicon["on_products_set_success"]

        self.on_one_algorithm = self._lexicon["on_one_algorithm_click"]
        self.on_algorithm_consumption_set = self._lexicon[
            "on_algorithm_consumption_set"
        ]

        self.on_newsletter_yes = self._lexicon["on_newsletter_yes_click"]
        self.on_newsletter_no_or_before_yes = self._lexicon["on_newsletter_no_click"]
        self.on_newsletter_end = self._lexicon["on_newsletter_create_end"]
        self.on_newsletter_bad_video_photo = self._lexicon[
            "on_newsletter_bad_video_photo_send"
        ]
        self.on_newsletter_start_quantity = self._lexicon[
            "on_newsletter_start_quantity"
        ]
        self.on_newsletter_end_quantity = self._lexicon["on_newsletter_end_quantity"]

        self.on_user_menu = self._lexicon["on_user_menu_click"]


class LexiconMsgKbName:
    def __init__(self, lexicon: dict) -> None:
        self._lexicon = lexicon["msg_kb_name"]
        self.yes = LexiconMsgKbNameReplyInline(self._lexicon["yes"])
        self.no = LexiconMsgKbNameReplyInline(self._lexicon["no"])
        self.prev = LexiconMsgKbNameReplyInline(self._lexicon["prev"])
        self.next = LexiconMsgKbNameReplyInline(self._lexicon["next"])
        self.cancel = LexiconMsgKbNameReplyInline(self._lexicon["cancel"])
        self.back = LexiconMsgKbNameReplyInline(self._lexicon["back"])
        self.algorithm = LexiconMsgKbNameReplyInline(self._lexicon["algorithm"])
        self.back_to_main_menu = LexiconMsgKbNameReplyInline(
            self._lexicon["back_to_main_menu"]
        )
        self.no_category_in_db = LexiconMsgKbNameReplyInline(
            self._lexicon["no_category_in_db"]
        )
        self.no_algorithm_in_db = LexiconMsgKbNameReplyInline(
            self._lexicon["no_algorithm_in_db"]
        )
        self.main_menu = LexiconMsgKbNameReplyInline(self._lexicon["main_manu"])
        self.calculator = LexiconMsgKbNameReplyInline(self._lexicon["calculator"])
        self.price_setter = LexiconMsgKbNameReplyInline(self._lexicon["price_setter"])

        self.admin_menu = LexiconMsgKbNameReplyInline(self._lexicon["admin_menu"])
        self.newsletter = LexiconMsgKbNameReplyInline(self._lexicon["newsletter"])
        self.products_provider = LexiconMsgKbNameReplyInline(
            self._lexicon["products_provider"]
        )
        self.products_set_new = LexiconMsgKbNameReplyInline(
            self._lexicon["products_set_new"]
        )
        self.user_menu = LexiconMsgKbNameReplyInline(self._lexicon["user_menu"])


class LexiconMsgKbNameReplyInline:
    def __init__(self, lexicon: dict[str, str | dict[str, str]]) -> None:
        self.reply = lexicon["reply"]
        self.inline = lexicon["inline"]
