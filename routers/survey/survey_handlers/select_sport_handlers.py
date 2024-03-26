from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from keyboards.common_keyboards import build_select_keyboard, build_yes_or_no_keyboard
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

known_f1_tracks_kb = build_select_keyboard(KnownF1Tracks)
known_sport_to_kb: dict = {
    KnownSports.formula_one: known_f1_tracks_kb,
}


@router.message(
    Survey.sport,
    F.text.cast(KnownSports),
)
async def select_sport(message: types.Message, state: FSMContext):
    next_state, question_text = known_sport_to_next[message.text]
    await state.update_data(
        sport=message.text,
        sport_question=question_text,
    )
    await state.set_state(next_state)
    kb = types.ReplyKeyboardRemove()
    if message.text in known_sport_to_kb:
        kb = known_sport_to_kb[message.text]
    await message.answer(
        text=question_text,
        reply_markup=kb,
    )


@router.message(Survey.sport)
async def select_sport_invalid_choice(message: types.Message):
    await message.answer(
        "Unknown sport, please select one of the following:",
        reply_markup=build_select_keyboard(KnownSports),
    )


@router.message(
    F.text,
    StateFilter(
        SurveySportDetails.tennis,
        SurveySportDetails.football,
    ),
)
@router.message(
    F.text.cast(KnownF1Tracks),
    SurveySportDetails.formula_one,
)
async def handle_selected_sport_details_option(
    message: types.Message,
    state: FSMContext,
):
    await state.update_data(sport_answer=message.text)
    await state.set_state(Survey.email_newsletter)
    await message.answer(
        text=(
            "Would you like to be notified about this sport? Email newsletter.\n"
            "This is last step, but you can /cancel any time."
        ),
        reply_markup=build_yes_or_no_keyboard(),
    )


@router.message(SurveySportDetails.tennis)
async def handle_tennis_player_not_text(message: types.Message):
    await message.answer(text="Please name tennis player using text.")


@router.message(SurveySportDetails.football)
async def handle_football_team_not_text(message: types.Message):
    await message.answer(text="Please name football team using text.")


@router.message(SurveySportDetails.formula_one)
async def handle_formula_one_not_one_of_tracks(message: types.Message):
    await message.answer(
        text="Please select one of known F1 tracks:",
        reply_markup=known_f1_tracks_kb,
    )
