from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram.utils import markdown

from routers.survey.states import Survey

router = Router(name=__name__)


@router.message(Survey.full_name, F.text)
async def handle_survey_user_full_name(
    message: types.Message,
    state: FSMContext,
) -> SendMessage:
    await state.update_data(full_name=message.text)
    await state.set_state(Survey.email)
    return message.answer(
        f"Hello, {markdown.hbold(message.text)}, now please share your email",
        parse_mode=ParseMode.HTML,
    )


@router.message(Survey.full_name)
async def handle_survey_user_full_name_invalid_content_type(
    message: types.Message,
) -> SendMessage:
    return message.answer(
        "Sorry, I didn't understand, send your full name as text. /cancel ?",
    )
