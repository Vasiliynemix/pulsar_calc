from src.bot.keyboards.admin_menu import AdminMenuKeyboard
from src.bot.keyboards.main_menu import MainMenuKeyboard
from src.bot.lexicon.lexicon import LexiconMsgKbName


class Keyboard:
    def __init__(self, kb_name: LexiconMsgKbName) -> None:
        self._kb_name = kb_name
        self.main_menu_kb = MainMenuKeyboard(self._kb_name)
        self.admin_menu_kb = AdminMenuKeyboard(self._kb_name)
