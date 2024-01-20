from typing import Final, List, Union
from os import environ

BOT_TOKEN: Final[str] = environ.get("BOT_TOKEN")
SENDER_API_LINK: Final[str] = environ.get("SENDER_API")


class Settings:
    TG_BOT_TOKEN: str = BOT_TOKEN
    ADMINS: Final[List[Union[int, str]]] = []
    SENDER_API: Final[str] = SENDER_API_LINK


settings = Settings()
