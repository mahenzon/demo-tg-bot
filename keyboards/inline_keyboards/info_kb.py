from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .actions_kb import random_num_updated_cb_data

random_num_dice_cb_data = "random_num_dice_cb_data"
random_num_modal_cb_data = "random_num_modal_cb_data"


def build_info_kb() -> InlineKeyboardMarkup:
    tg_channel_btn = InlineKeyboardButton(
        text="📣 Канал",
        url="https://t.me/Khorenyan",
    )
    tg_chat_btn = InlineKeyboardButton(
        text="💬 Чат",
        url="https://t.me/SurenTalk",
    )
    bot_source_code_btn = InlineKeyboardButton(
        text="🤖 Исходный код этого бота",
        url="https://github.com/mahenzon/demo-tg-bot",
    )
    btn_random_site = InlineKeyboardButton(
        text="Random number message",
        callback_data=random_num_updated_cb_data,
    )
    btn_random_num = InlineKeyboardButton(
        text="🎲 Random Num",
        callback_data=random_num_dice_cb_data,
    )
    btn_random_num_modal = InlineKeyboardButton(
        text="👾 Random Number",
        callback_data=random_num_modal_cb_data,
    )
    row_tg = [tg_channel_btn, tg_chat_btn]
    # row_first = [tg_channel_btn]
    # row_second = [tg_chat_btn]
    rows = [
        # row_first,
        # row_second,
        row_tg,
        [bot_source_code_btn],
        [btn_random_site],
        [btn_random_num],
        [btn_random_num_modal],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup
