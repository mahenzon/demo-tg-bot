from random import randint

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


random_num_updated_cb_data = "random_num_updated_cb_data"


class FixedRandomNumCbData(CallbackData, prefix="fixed-random-num"):
    number: int


def build_actions_kb(
    random_number_button_text="Random number",
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=random_number_button_text,
        callback_data=random_num_updated_cb_data,
    )
    cb_data_1 = FixedRandomNumCbData(number=randint(1, 100))
    builder.button(
        text=f"Random number: {cb_data_1.number}",
        callback_data=cb_data_1.pack(),
    )
    builder.button(
        text="Random number: [HIDDEN]",
        callback_data=FixedRandomNumCbData(number=randint(1, 100)).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()
