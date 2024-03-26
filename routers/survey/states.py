from enum import StrEnum

from aiogram.fsm.state import StatesGroup, State


class Survey(StatesGroup):
    full_name = State()
    email = State()
    sport = State()
    email_newsletter = State()


class SurveySportDetails(StatesGroup):
    tennis = State()
    football = State()
    formula_one = State()


class KnownSports(StrEnum):
    tennis = "Tennis"
    football = "Football"
    formula_one = "Formula One"


class KnownF1Tracks(StrEnum):
    monaco = "Monaco"
    spa = "Spa"
    suzuka = "Suzuka"
    monza = "Monza"
