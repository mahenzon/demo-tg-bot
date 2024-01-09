from re import Match

from aiogram import Router, F, types
from magic_filter import RegexpMode

from config import settings

router = Router(name=__name__)


@router.message(F.from_user.id.in_(settings.admin_ids), F.text == "secret")
async def secret_admin_message(message: types.Message):
    await message.reply("Hi, admin!")


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.regexp(r"(\d+)", mode=RegexpMode.MATCH).as_("code"),
)
async def handle_code(message: types.Message, code: Match[str]):
    await message.reply(f"Your code: {code.group()}")
