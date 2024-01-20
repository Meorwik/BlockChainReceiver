from aiogram.enums.parse_mode import ParseMode
from aiogram import Dispatcher, Bot
from .settings import settings

receiver = Bot(token=settings.TG_BOT_TOKEN, parse_mode=ParseMode.HTML)
dispatcher = Dispatcher()
