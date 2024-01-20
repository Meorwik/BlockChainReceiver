from receiver.config.bot import dispatcher
from aiogram import Router


menus_router = Router(name="Menus")
dispatcher.include_router(menus_router)
