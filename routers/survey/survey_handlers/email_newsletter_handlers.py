from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from keyboards.common_keyboards import build_yes_or_no_keyboard
from routers.survey.states import Survey

router = Router(name=__name__)


async def send_survey_results(message: types.Message, data: dict) -> None:
    text = markdown.text(
        markdown.hunderline("Your survey results:"),
        "",
        markdown.text("Name:", markdown.hbold(data["full_name"])),
        markdown.text("Email:", markdown.hcode(data["email"])),
        "",
        markdown.text("Preferred sport:", markdown.hbold(data["sport"])),
        markdown.text("Q:", markdown.hitalic(data["sport_question"])),
        markdown.text("A:", markdown.hitalic(data["sport_answer"])),
        "",
        (
            "Cool, we'll send you our news!"
            if data["newsletter_ok"]
            else "And we won't bother you again."
        ),
        sep="\n",
    )
    await message.answer(
        text=text,
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(Survey.email_newsletter, F.text.casefold() == "yes")
async def handle_survey_email_newsletter_ok(
    message: types.Message,
    state: FSMContext,
):
    data = await state.update_data(newsletter_ok=True)
    await state.clear()
    await send_survey_results(message, data)


@router.message(Survey.email_newsletter, F.text.casefold() == "no")
async def handle_survey_email_newsletter_not_ok(
    message: types.Message,
    state: FSMContext,
):
    data = await state.update_data(newsletter_ok=False)
    await state.clear()
    await send_survey_results(message, data)


@router.message(Survey.email_newsletter)
async def handle_survey_email_newsletter_could_not_understand(message: types.Message):
    await message.answer(
        text=(
            "Sorry, I didn't understand, "
            f"please send {markdown.hcode('yes')} or {markdown.hcode('no')}"
        ),
        reply_markup=build_yes_or_no_keyboard(),
    )
