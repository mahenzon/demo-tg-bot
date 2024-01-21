from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButtonPollType,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class ButtonText:
    HELLO = "Hello!"
    WHATS_NEXT = "What's next?"
    BYE = "Bye-bye"


def get_on_start_kb() -> ReplyKeyboardMarkup:
    button_hello = KeyboardButton(text=ButtonText.HELLO)
    button_help = KeyboardButton(text=ButtonText.WHATS_NEXT)
    button_bye = KeyboardButton(text=ButtonText.BYE)
    buttons_first_row = [button_hello, button_help]
    buttons_second_row = [button_bye]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row, buttons_second_row],
        resize_keyboard=True,
        # one_time_keyboard=True,
    )
    return markup


def get_on_help_kb() -> ReplyKeyboardMarkup:
    numbers = [
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣",
        "0️⃣",
    ]
    buttons_row = [KeyboardButton(text=num) for num in numbers]
    # buttons_row.append(buttons_row[0])
    # buttons_row.append(buttons_row[1])
    # # buttons_row.append(buttons_row[2])
    # # buttons_row.pop(0)
    #
    # markup = ReplyKeyboardMarkup(
    #     keyboard=[buttons_row, buttons_row],
    #     resize_keyboard=True,
    # )
    # return markup
    builder = ReplyKeyboardBuilder()
    for num in numbers:
        # builder.button(text=num)
        builder.add(KeyboardButton(text=num))
    # builder.adjust(3, 3, 4)
    builder.adjust(3)
    builder.row(buttons_row[3], buttons_row[1])
    builder.add(buttons_row[-1])
    return builder.as_markup(resize_keyboard=False)


def get_actions_kb() -> ReplyKeyboardMarkup:
    # markup = ReplyKeyboardMarkup(
    #     input_field_placeholder=""
    # #     keyboard=[]
    # )

    # return markup
    builder = ReplyKeyboardBuilder()
    # builder.add(KeyboardButton(text="🌍 Send Location", request_location=True))
    builder.button(
        text="🌍 Send Location",
        request_location=True,
    )
    builder.button(
        text="☎️ Send My Phone",
        request_contact=True,
    )
    builder.button(
        text="📊 Send Poll",
        request_poll=KeyboardButtonPollType(),
    )
    builder.button(
        text="👾 Send Quiz",
        request_poll=KeyboardButtonPollType(type="quiz"),
    )
    builder.button(
        text="🍽️ Dinner?",
        request_poll=KeyboardButtonPollType(type="regular"),
    )
    builder.button(text=ButtonText.BYE)
    builder.adjust(1)
    return builder.as_markup(
        input_field_placeholder="Actions:",
        resize_keyboard=True,
    )
