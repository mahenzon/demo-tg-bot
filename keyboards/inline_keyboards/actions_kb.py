from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


random_num_updated_cb_data = "random_num_updated_cb_data"


def build_actions_kb(
    random_number_button_text="Random number",
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=random_number_button_text,
        callback_data=random_num_updated_cb_data,
    )
    return builder.as_markup()
