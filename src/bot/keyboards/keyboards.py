from src.bot.keyboards.admin_menu import AdminMenuKeyboard
from src.bot.keyboards.main_menu import MainMenuKeyboard
from src.bot.lexicon.lexicon import LexiconMsgKbName
from src.config import Config


class Keyboard:
    def __init__(self, kb_name: LexiconMsgKbName, cfg: Config) -> None:
        self._kb_name = kb_name
        self.main_menu_kb = MainMenuKeyboard(self._kb_name, cfg)
        self.admin_menu_kb = AdminMenuKeyboard(self._kb_name)
