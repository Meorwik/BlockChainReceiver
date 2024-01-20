from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import CallbackData
from typing import Final, Dict, List, Union
from ...data.texts import BACK_BUTTON_TEXT
from .callbacks import BackCallback
from abc import ABC


class BaseBuilder(InlineKeyboardBuilder, ABC):
    """
    This is a base abstract class that represents main logic and the way inline menus and keyboards are created

    '__name__' must be overriden by inherited class for visual separating in system with '__repr__' method
    """

    __name__ = "BaseBuilder"

    def __repr__(self):
        return f"{self.__name__}Object - ({id(self)})"

    def _init_keyboard(self) -> None:
        """
        This method MUST br called in 'get_keyboard' method in order to provide successful initialization of keyboard.
        Override this method in inherited classes for your purpose in order to create your own keyboard automatically.

        :return: None
        """
        ...

    def get_keyboard(self) -> InlineKeyboardMarkup:
        """
        This method must include small amount of code, this method is responsible for separating keyboard levels.
        In case if you don't know from which place in your this method will be called, create 'level' variable in your
        inherited class and separate work of your menus on different levels.

        :returns: InlineKeyboardMarkup keyboard based on current level.

        :example:
            def get_keyboard(self) -> InlineKeyboardMarkup:
                if (self.level) == "level":
                    return (your_keyboard)

                else:
                    ...
        """
        ...


class InlineBuilder(BaseBuilder):
    __name__ = "InlineBuilder"
    _BACK_BUTTON_TEXT: str = BACK_BUTTON_TEXT
    __BASE_LEVEL: Final[str] = "MainMenu"
    __BASE_BACK_BUTTON_CALLBACK: CallbackData = BackCallback(go_to=__BASE_LEVEL)
    _ADJUST_SIZES: List[int] = []
    _LEVEL: str = __BASE_LEVEL

    def __init__(self, level: str = None):
        super().__init__()
        if level is None:
            self.level: str = self.__BASE_LEVEL

        else:
            self.level: str = level

    @classmethod
    def get_menu_level(cls):
        return cls._LEVEL

    def get_back_button(self, back_callback: Union[BackCallback, str] = None) -> InlineKeyboardButton:
        """
        This method is for adding a 'back' button that leads to previous menu

        :param back_callback: Union[BackCallback, str]
        :return: InlineKeyboardButton
        """

        if back_callback is None:
            return InlineKeyboardButton(
                text=self._BACK_BUTTON_TEXT,
                callback_data=self.__BASE_BACK_BUTTON_CALLBACK.pack()
            )
        else:
            if isinstance(back_callback, BackCallback):
                back_callback = back_callback.pack()

            return InlineKeyboardButton(
                text=self._BACK_BUTTON_TEXT,
                callback_data=back_callback
            )

    def get_back_button_keyboard(self, back_callback: Union[BackCallback, str] = None) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[[self.get_back_button(back_callback)]])

    def get_keyboard(self) -> InlineKeyboardMarkup:
        self._init_keyboard()

        if self.level != self.__BASE_LEVEL:
            self.add(self.get_back_button())

        self.adjust(*self._ADJUST_SIZES)
        return self.as_markup()


class FacadeKeyboard(InlineBuilder):
    """
    FacadeKeyboards can be used in different 2 ways.
        -- Dynamic button generation
        -- Static buttons and static callbacks


    How to use static way:
        - Define your menu by overriding '_FACADE' with your buttons by using
        {
            "button_name": "button_callback"
            "button_name2": "button_callback2"
                          ...
            ...e.t.c
        }

    How to use dynamic way:
        - Define your menu by overriding '_init_facade' method, must return Dict with following format:
        {
            "button_name": "button_callback"
            "button_name2": "button_callback2"
                          ...
            ...e.t.c
        }

    """

    __name__ = "StaticKeyboard"

    __DEFAULT_FACADE: Dict[str, Union[str, CallbackData]] = {
        "button1": "button1_callback",
        "button2": "button2_callback",
        "button3": "button3_callback",
    }

    _FACADE: Dict[str, Union[str, CallbackData]] = __DEFAULT_FACADE

    def __init__(self, level: str = None):
        super().__init__(level)
        if self._FACADE == self.__DEFAULT_FACADE:
            self._FACADE = self._init_facade()

    def _init_facade(self) -> Dict:
        return {}

    def _init_keyboard(self) -> None:
        menu_buttons: List[InlineKeyboardButton] = [
            InlineKeyboardButton(text=key, callback_data=value)
            for key, value
            in self._FACADE.items()
        ]
        self.add(*menu_buttons)

