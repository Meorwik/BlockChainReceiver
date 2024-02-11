from ...keyboards.inline.inline_menus import MainMenuBuilder, RedirectsMenuBuilder, ConfirmationKeyboardBuilder
from ...keyboards.inline.callbacks import BackCallback, ActionCallback, RedirectCallback
from ...states.states import RequestForRedirectData, RequestForConfirmation
from ...utils.sender_controller import SenderAPIController
from ...utils.data_prettifier import DataPrettifier
from aiogram.types import CallbackQuery, Message
from ..commands.start import reopen_main_menu
from ...utils.redirect_model import Redirect
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from .base import menus_router
from typing import List, Dict
from aiogram import F, Router
from ...data import texts


main_menu = Router(name="MainMenu")
menus_router.include_router(main_menu)
sender_api_controller = SenderAPIController()
data_prettifier = DataPrettifier()
main_menu_builder = MainMenuBuilder()


async def open_choose_redirect_menu(call: CallbackQuery, state: FSMContext):
    redirects_data: List = sender_api_controller.read_all_redirects()["info"]

    if redirects_data:
        redirects_menu = RedirectsMenuBuilder(redirects_data)
        await call.message.edit_text(
            text=texts.EDIT_REDIRECT_TEXT,
            reply_markup=redirects_menu.get_keyboard()
        )
        await state.set_state(RequestForRedirectData.get_redirect_id)

    else:
        await call.message.edit_text(
            text=texts.EMPTY_REDIRECTS_LIST_CASE,
            reply_markup=main_menu_builder.get_back_button_keyboard()
        )


@main_menu.callback_query(BackCallback.filter(F.go_to), StateFilter("*"))
async def handle_back_button(call: CallbackQuery, state: FSMContext):
    callback = BackCallback.unpack(call.data)

    if callback.go_to == MainMenuBuilder.get_menu_level():
        await reopen_main_menu(call.message, state)


@main_menu.callback_query(ActionCallback.filter(F.menu_level == MainMenuBuilder.get_menu_level()), StateFilter(None))
async def handle_main_menu(call: CallbackQuery, state: FSMContext):
    callback = ActionCallback.unpack(call.data)

    default_storage = {
        "action": callback.action,
        "redirect": Redirect(),
    }

    await state.set_data(default_storage)

    if callback.action == "show_all_redirects":
        data = sender_api_controller.read_all_redirects()
        redirects: List[Dict] = data["info"]
        if redirects:
            redirects_showcase: str = await data_prettifier.prettify_redirects_info(redirects)
        else:
            redirects_showcase: str = texts.EMPTY_REDIRECTS_LIST_CASE

        await call.message.edit_text(redirects_showcase, reply_markup=main_menu_builder.get_back_button_keyboard())

    elif callback.action == "create_new_redirect":
        await state.set_state(RequestForRedirectData.get_copy_from_id)
        await call.message.edit_text(
            text=texts.CREATE_NEW_REDIRECT_TEXT,
            reply_markup=None
        )

    elif callback.action == "edit_redirect":
        await open_choose_redirect_menu(call, state)

    elif callback.action == "copy_chat_history":
        await state.set_state(RequestForRedirectData.get_copy_from_id)
        await call.message.edit_text(
            text=texts.ASK_FOR_COPY_FROM_CHAT_ID_TEXT,
            reply_markup=None
        )

    elif callback.action == "delete_one_redirect":
        await open_choose_redirect_menu(call, state)

    elif callback.action == "delete_all_redirects":
        await state.set_state(RequestForConfirmation.get_confirmation)
        await call.message.edit_text(
            text=texts.ASK_CONFIRMATION_FOR_DELETING_ALL,
            reply_markup=ConfirmationKeyboardBuilder().get_keyboard()
        )


@main_menu.callback_query(StateFilter(RequestForRedirectData.get_redirect_id), RedirectCallback.filter(F.redirect))
async def handle_passing_redirect_id_data(call: CallbackQuery, state: FSMContext):
    redirect_data = RedirectCallback.unpack(call.data)

    state_data: Dict = await state.get_data()
    state_data["redirect"].id = redirect_data.redirect
    action = state_data["action"]

    if action == "delete_one_redirect":
        await state.set_state(RequestForConfirmation.get_confirmation)
        await call.message.edit_text(
            text=texts.ASK_CONFIRMATION_FOR_DELETING_ONE,
            reply_markup=ConfirmationKeyboardBuilder().get_keyboard()
        )

    else:
        await state.set_data(state_data)
        await state.set_state(RequestForRedirectData.get_copy_from_id)

        await call.message.edit_text(
            text=texts.ASK_FOR_COPY_FROM_CHAT_ID_TEXT,
            reply_markup=None
        )


@main_menu.message(StateFilter(RequestForRedirectData.get_copy_from_id))
async def handle_passing_redirect_copy_from_data(message: Message, state: FSMContext):
    if sender_api_controller.is_valid_chat(message.text)["info"]:
        state_data: Dict = await state.get_data()
        state_data["redirect"].copy_from = message.text
        await state.set_data(state_data)

        await state.set_state(RequestForRedirectData.get_copy_to_id)
        await message.answer(
            text=texts.ASK_FOR_COPY_TO_CHAT_ID_TEXT,
            reply_markup=None
        )

    else:
        await message.answer(texts.ASK_TO_TRY_AGAIN)


@main_menu.message(StateFilter(RequestForRedirectData.get_copy_to_id))
async def handle_passing_redirect_copy_to_data(message: Message, state: FSMContext):
    if sender_api_controller.is_valid_chat(message.text)["info"]:
        state_data: Dict = await state.get_data()
        state_data["redirect"].copy_to = message.text
        action = state_data["action"]
        await state.set_data(state_data)

        if action == "create_new_redirect":
            await state.set_state(RequestForConfirmation.get_confirmation)
            await message.answer(
                text=texts.ASK_CONFIRMATION_FOR_ADDING_NEW_REDIRECT,
                reply_markup=ConfirmationKeyboardBuilder().get_keyboard()
            )

        elif action == "edit_redirect":
            await state.set_state(RequestForConfirmation.get_confirmation)
            await message.answer(
                text=texts.ASK_CONFIRMATION_FOR_EDITING_REDIRECT,
                reply_markup=ConfirmationKeyboardBuilder().get_keyboard()
            )

        elif action == "copy_chat_history":
            await state.set_state(RequestForConfirmation.get_confirmation)
            await message.answer(
                text=texts.ASK_CONFIRMATION_FOR_COPY_HISTORY,
                reply_markup=ConfirmationKeyboardBuilder().get_keyboard()
            )

    else:
        await message.answer(texts.ASK_TO_TRY_AGAIN)


@main_menu.callback_query(StateFilter(RequestForConfirmation.get_confirmation))
async def handle_getting_confirmation(call: CallbackQuery, state: FSMContext):
    if call.data == "ConfirmationStatus - YES":
        await call.message.edit_text(texts.OPERATION_IN_PROCESS_TEXT)
        state_data = await state.get_data()
        action = state_data["action"]
        redirect = state_data["redirect"]

        if action == "create_new_redirect":
            result = sender_api_controller.create_redirect(
                copy_from=redirect.copy_from,
                copy_to=redirect.copy_to
            )["info"]

        elif action == "edit_redirect":
            result = sender_api_controller.update_redirect(
                redirect_id=redirect.id,
                copy_from=redirect.copy_from,
                copy_to=redirect.copy_to
            )["info"]

        elif action == "copy_chat_history":
            result = sender_api_controller.copy_history(
                copy_from=redirect.copy_from,
                copy_to=redirect.copy_to
            )["info"]

        elif action == "delete_one_redirect":
            result = sender_api_controller.delete_redirect(
                redirect_id=redirect.id
            )["info"]

        elif action == "delete_all_redirects":
            result = sender_api_controller.delete_all_redirects()["info"]

        else:
            result = False

        is_successful = bool(result)

        if is_successful:
            await call.message.edit_text(
                text="Все прошло успешно!",
                reply_markup=main_menu_builder.get_back_button_keyboard()
            )
            await state.clear()

    elif call.data == "ConfirmationStatus - NO":
        await reopen_main_menu(call.message, state)

