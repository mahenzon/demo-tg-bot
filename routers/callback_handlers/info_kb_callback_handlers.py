from random import randint

from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline_keyboards.info_kb import (
    random_num_dice_cb_data,
    random_num_modal_cb_data,
)

router = Router(name=__name__)


@router.callback_query(F.data == random_num_dice_cb_data)
async def handle_random_num_dice_cb(callback_query: CallbackQuery):
    await callback_query.answer(
        text=f"Your random dice: {randint(1, 21)}",
        cache_time=5,
    )


@router.callback_query(F.data == random_num_modal_cb_data)
async def handle_random_num_modal_cb(callback_query: CallbackQuery):
    await callback_query.answer(
        text=f"Random num: {randint(1, 100)}",
        cache_time=9,
        show_alert=True,
    )
