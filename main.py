from receiver.config.bot import dispatcher, receiver
from receiver_logging import receiver_logging
import asyncio
from receiver import handlers
from receiver.handlers.users import main_menu
from receiver.handlers.commands import start


async def start_receiver():
    await dispatcher.start_polling(receiver)


if __name__ == "__main__":
    asyncio.run(start_receiver())
