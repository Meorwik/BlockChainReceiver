from receiver.config.bot import dispatcher
from aiogram import Router

commands = Router(name="Commands")
dispatcher.include_router(commands)