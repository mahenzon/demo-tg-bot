from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from .survey_handlers.email_newsletter_handlers import (
    router as email_newsletter_router,
)
from .survey_handlers.user_email_handlers import (
    router as user_email_router,
)
from .survey_handlers.full_name import router as full_name_router
from .survey_handlers.select_sport_handlers import router as select_sport_router

from .states import Survey, SurveySportDetails

router = Router(name=__name__)
router.include_router(full_name_router)
router.include_router(user_email_router)
router.include_router(select_sport_router)
router.include_router(email_newsletter_router)


@router.message(
    Command("survey", prefix="!/"),
    default_state,
)
async def handle_start_survey(message: types.Message, state: FSMContext):
    await state.set_state(Survey.full_name)
    await message.answer(
        "Welcome to our weekly survey! What's your name?",
        reply_markup=types.ReplyKeyboardRemove(),
    )


survey_states = StateFilter(
    Survey(),
    SurveySportDetails(),
)


@router.message(Command("cancel"), survey_states)
@router.message(F.text.casefold() == "cancel", survey_states)
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel survey
    """
    current_state = await state.get_state()
    await state.clear()
    await message.answer(
        f"Cancelled survey on step {current_state}. Start again: /survey",
        reply_markup=types.ReplyKeyboardRemove(),
    )
