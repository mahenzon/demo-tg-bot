from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from keyboards.common_keyboards import build_select_keyboard
from routers.survey.states import (
    Survey,
    SurveySportDetails,
    KnownSports,
    KnownF1Tracks,
)

router = Router(name=__name__)


known_sport_to_next: dict[KnownSports | str, tuple[State, str]] = {
    KnownSports.tennis: (
        SurveySportDetails.tennis,
        "Who is your favourite tennis player?",
    ),
    KnownSports.football: (
        SurveySportDetails.football,
        "What is your favourite football team?",
    ),
    KnownSports.formula_one: (
        SurveySportDetails.formula_one,
        "What is your favourite formula track?",
    ),
}

known_sport_to_kb: dict = {
    KnownSports.formula_one: build_select_keyboard(KnownF1Tracks),
}


@router.message(
    Survey.sport,
    # F.text.in_(KnownSports),
    F.text.cast(KnownSports),
    # F.text == KnownSports.tennis,
)
async def select_sport(message: types.Message, state: FSMContext):
    await state.update_data(sport=message.text)
    next_state, question_text = known_sport_to_next[message.text]
    await state.set_state(next_state)
    kb = types.ReplyKeyboardRemove()
    if message.text in known_sport_to_kb:
        kb = known_sport_to_kb[message.text]
    await message.answer(
        text=question_text,
        reply_markup=kb,
    )


@router.message(Survey.sport)
async def select_sport(message: types.Message):
    await message.answer(
        "Unknown sport, please select one of the following:",
        reply_markup=build_select_keyboard(KnownSports),
    )
