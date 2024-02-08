from random import randint

from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline_keyboards.info_kb import (
    RandomNumAction,
    RandomNumCbData,
)

router = Router(name=__name__)


@router.callback_query(
    RandomNumCbData.filter(F.action == RandomNumAction.dice),
)
async def handle_random_num_dice_cb(callback_query: CallbackQuery):
    await callback_query.answer(
        text=f"Your random dice: {randint(1, 21)}",
        cache_time=5,
    )


@router.callback_query(
    RandomNumCbData.filter(F.action == RandomNumAction.modal),
)
async def handle_random_num_modal_cb(callback_query: CallbackQuery):
    await callback_query.answer(
        text=f"Random num: {randint(1, 100)}",
        cache_time=9,
        show_alert=True,
    )
