from aiogram.fsm.state import StatesGroup, State


class Survey(StatesGroup):
    full_name = State()
    email = State()
    email_newsletter = State()
