from re import Match

from aiogram import Router, F, types
from aiogram.utils import markdown
from magic_filter import RegexpMode

from config import settings
from middlewares.rate_limit_middleware import RateLimitInfo

router = Router(name=__name__)


@router.message(F.from_user.id.in_(settings.admin_ids), F.text == "secret")
async def secret_admin_message(message: types.Message):
    await message.reply("Hi, admin!")


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.regexp(r"(\d+)", mode=RegexpMode.MATCH).as_("code"),
)
async def handle_code(
    message: types.Message,
    code: Match[str],
    rate_limit_info: RateLimitInfo,
    # rate_limit_info: RateLimitInfo | None = None,
):
    count = rate_limit_info.message_count
    first_msg = rate_limit_info.first_message
    text = markdown.text(
        f"Your code: {code.group()}\n",
        f"RL messages count: {count}",
        f"RL first message: {first_msg}",
        sep="\n",
    )
    await message.reply(text=text)
