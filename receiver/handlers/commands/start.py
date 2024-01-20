from receiver.keyboards.inline.inline_menus import MainMenuBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.filters import StateFilter
from aiogram.types import Message
from receiver.data import texts
from aiogram import Router
from .base import commands


start_router = Router(name="start")
commands.include_router(start_router)


async def open_main_menu(message: Message, state: FSMContext):
    await state.clear()
    main_menu: MainMenuBuilder = MainMenuBuilder().get_keyboard()
    await message.answer(
        text=texts.GREETING_TEXT,
        reply_markup=main_menu
    )


async def reopen_main_menu(message: Message, state: FSMContext):
    await state.clear()
    main_menu: MainMenuBuilder = MainMenuBuilder().get_keyboard()
    await message.edit_text(
        text=texts.GREETING_TEXT,
        reply_markup=main_menu
    )


@start_router.message(CommandStart(), StateFilter("*"))
async def handle_command_start(message: Message, state: FSMContext):
    await open_main_menu(message, state)
