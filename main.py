import asyncio
import logging
from re import Match

from magic_filter import RegexpMode

from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode

from config import settings

dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    url = "https://w7.pngwing.com/pngs/547/380/png-transparent-robot-waving-hand-bot-ai-robot-thumbnail.png"
    await message.answer(
        text=f"{markdown.hide_link(url)}Hello, {markdown.hbold(message.from_user.full_name)}!",
        parse_mode=ParseMode.HTML,
    )


@dp.message(Command("help", prefix="!/"))
async def handle_help(message: types.Message):
    # text = "I'm an echo bot.\nSend me any message!"
    # entity_bold = types.MessageEntity(
    #     type="bold",
    #     offset=len("I'm an echo bot.\nSend me "),
    #     length=3,
    # )
    # entities = [entity_bold]
    # await message.answer(text=text, entities=entities)
    text = markdown.text(
        markdown.markdown_decoration.quote("I'm an {echo} bot."),
        markdown.text(
            "Send me",
            markdown.markdown_decoration.bold(
                markdown.text(
                    markdown.underline("literally"),
                    "any",
                ),
            ),
            markdown.markdown_decoration.quote("message!"),
        ),
        sep="\n",
    )
    await message.answer(
        text=text,
        # parse_mode=None,
        # parse_mode=ParseMode.MARKDOWN_V2,
    )


@dp.message(Command("code", prefix="/!%"))
async def handle_command_code(message: types.Message):
    text = markdown.text(
        "Here's Python code:",
        "",
        markdown.markdown_decoration.pre_language(
            # markdown.markdown_decoration.pre(
            markdown.text(
                "print('Hello world!')",
                "\n",
                "def foo():\n    return 'bar'",
                sep="\n",
            ),
            language="python",
        ),
        "And here's some JS:",
        "",
        markdown.markdown_decoration.pre_language(
            markdown.text(
                "console.log('Hello world!')",
                "\n",
                "function foo() {\n  return 'bar'\n}",
                sep="\n",
            ),
            language="javascript",
        ),
        sep="\n",
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


# @dp.message(is_photo)
# @dp.message(lambda message: message.photo)
@dp.message(F.photo, ~F.caption)
async def handle_photo_wo_caption(message: types.Message):
    await message.reply("I can't see, sorry. Could you describe it please?")


@dp.message(F.photo, F.caption.contains("please"))
async def handle_photo_with_please_caption(message: types.Message):
    await message.reply("Don't beg me. I can't see, sorry.")


any_media_filter = F.photo | F.video | F.document


@dp.message(any_media_filter, ~F.caption)
# @dp.message(F.photo, F.video, ~F.caption)
# @dp.message(F.photo | F.video | F.document, ~F.caption)
async def handle_any_media_wo_caption(message: types.Message):
    await message.reply("I can't see.")


@dp.message(any_media_filter, F.caption)
async def handle_any_media_w_caption(message: types.Message):
    await message.reply(f"Smth is on media. Your text: {message.caption!r}")


@dp.message(F.from_user.id.in_({42, 3595399}), F.text == "secret")
async def secret_admin_message(message: types.Message):
    await message.reply("Hi, admin!")


# @dp.message(F.text.regexp(r"(\d+)", mode=RegexpMode.FINDALL).as_("code"))
# async def handle_code(message: types.Message, code: list[str]):
#     await message.reply(f"Your code: {code}")


@dp.message(F.text.regexp(r"(\d+)", mode=RegexpMode.MATCH).as_("code"))
async def handle_code(message: types.Message, code: Match[str]):
    await message.reply(f"Your code: {code.group()}")


@dp.message()
async def echo_message(message: types.Message):
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text="Start processing...",
    # )
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text="Detected message...",
    #     reply_to_message_id=message.message_id,
    # )

    await message.answer(
        text="Wait a second...",
        parse_mode=None,
    )
    # if message.text:
    #     await message.answer(
    #         text=message.text,
    #         entities=message.entities,
    #         parse_mode=None,
    #     )
    #     return
    try:
        await message.copy_to(chat_id=message.chat.id)
        # await message.forward(chat_id=message.chat.id)
        # await message.bot.forward_message(
        #     chat_id
        #     from_chat_id
        #     message_id
        # )
        # await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new 🙂")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.bot_token,
        # parse_mode=ParseMode.MARKDOWN_V2,
        parse_mode=ParseMode.HTML,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
