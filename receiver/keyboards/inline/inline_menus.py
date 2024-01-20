from .callbacks import ActionCallback, RedirectCallback
from ...utils.redirect_model import Redirect
from .inline_base import FacadeKeyboard
from typing import Final, List, Dict


class MainMenuBuilder(FacadeKeyboard):
    __name__ = "MainMenuBuilder"

    _ADJUST_SIZES: List[int] = [1]

    _ACTIONS: Final[Dict[str, str]] = {
        "show_all_redirects": "🔄 Показать все перенаправления",
        "create_new_redirect": "➕ Добавить перенаправление",
        "edit_redirect": "✏️ Изменить перенаправление",
        "copy_chat_history": "💬 Копировать историю чата",
        "delete_one_redirect": "✖️ Удалить одно перенаправление",
        "delete_all_redirects": "❌ Удалить все перенаправления"
    }

    def _init_facade(self) -> Dict:
        facade = {
            key: value
            for (key, value) in
            zip(
                self._ACTIONS.values(),
                [ActionCallback(menu_level=self.level, action=callback).pack() for callback in self._ACTIONS.keys()]
            )
        }
        return facade


class RedirectsMenuBuilder(FacadeKeyboard):
    __name__ = "RedirectsMenuBuilder"

    _LEVEL = "RedirectsMenu"
    _ADJUST_SIZES: List[int] = [1]

    def __init__(self, redirects_data: List[Dict]):
        self.redirects_data: List[Dict] = redirects_data
        super().__init__(self._LEVEL)

    def _init_facade(self) -> Dict:
        facade: Dict = {}
        for redirect in self.redirects_data:
            facade.update({
                f"{redirect['copy_from_name']} --> {redirect['copy_to_name']}": RedirectCallback(redirect=redirect["id"]).pack()
            })
        return facade


class ConfirmationKeyboardBuilder(FacadeKeyboard):
    __name__ = "ConfirmationKeyboardBuilder"

    _ADJUST_SIZES: List[int] = [2]

    _FACADE = {
        "✅ Да, подтверждаю": "ConfirmationStatus - YES",
        "❌ Нет, я передумал": "ConfirmationStatus - NO"
    }

