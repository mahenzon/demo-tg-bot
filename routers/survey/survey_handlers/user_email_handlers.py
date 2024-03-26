from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown
from email_validator import validate_email

from keyboards.common_keyboards import build_select_keyboard
from routers.survey.states import Survey, KnownSports

# from validators.email_validators import (
#     valid_email_filter,
#     valid_email_message_text,
#     valid_email,
# )

router = Router(name=__name__)


@router.message(
    Survey.email,
    # valid_email_filter,
    # F.func(valid_email_message_text).as_("email"),
    # F.text.cast(valid_email).as_("email"),
    F.text.cast(validate_email).normalized.as_("email"),
)
async def handle_survey_email_message(
    message: types.Message,
    state: FSMContext,
    email: str,
):
    await state.update_data(email=email)
    await state.set_state(Survey.sport)
    await message.answer(
        text=(
            f"Cool, your email is now {markdown.hcode(email)}.\n"
            "Which sport would you prefer?"
        ),
        reply_markup=build_select_keyboard(KnownSports),
    )


@router.message(Survey.email)
async def handle_survey_invalid_email_message(message: types.Message):
    await message.answer(
        text="Invalid email, please try again. Cancel survey? Tap /cancel",
    )
