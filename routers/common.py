from aiogram import Router, types
from aiogram.enums import ChatAction

router = Router(name=__name__)


@router.message()
async def echo_message(message: types.Message):
    await message.answer(
        text="Wait a second...",
        parse_mode=None,
    )
    if message.sticker:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.CHOOSE_STICKER,
        )
    try:
        await message.copy_to(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new 🙂")
