from aiogram.fsm.state import State, StatesGroup


class RequestForRedirectData(StatesGroup):
    get_redirect_id = State()
    get_copy_from_id = State()
    get_copy_to_id = State()


class RequestForConfirmation(StatesGroup):
    get_confirmation = State()
