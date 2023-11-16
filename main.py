import asyncio
import csv
import io
import logging
from re import Match

from aiogram.utils.chat_action import ChatActionSender
from magic_filter import RegexpMode

import aiohttp
from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types

from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode, ChatAction

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


@dp.message(Command("pic"))
async def handle_command_pic(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    url = "https://t4.ftcdn.net/jpg/00/97/58/97/360_F_97589769_t45CqXyzjz0KXwoBZT9PRaWGHRk5hQqQ.jpg"
    # url = "https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb"
    # file_path = "/Users/suren/Downloads/cat-small.jpg"
    # await message.bot.send_photo()
    await message.reply_photo(
        photo=url,
        # photo=types.FSInputFile(
        #     path=file_path,
        #     # filename=
        # ),
        # caption="cat small pic",
    )


@dp.message(Command("file"))
async def handle_command_file(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        # action=ChatAction.TYPING,
        # action=ChatAction.UPLOAD_PHOTO,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    file_path = "/Users/suren/Downloads/cat.jpeg"
    await message.reply_document(
        document=types.FSInputFile(
            path=file_path,
            filename="cat-big-photo.jpeg",
        ),
    )
    # message_sent.document.file_id


@dp.message(Command("text"))
async def send_txt_file(message: types.Message):
    file = io.StringIO()
    file.write("Hello, world!\n")
    file.write("This is a text file.\n")
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue().encode("utf-8"),
            filename="text.txt",
        ),
    )


@dp.message(Command("csv"))
async def send_csv_file(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    file = io.StringIO()
    csv_writer = csv.writer(file)
    csv_writer.writerows(
        [
            ["Name", "Age", "City"],
            ["John Smith", "28", "New York"],
            ["Jane Doe", "32", "Los Angeles"],
            ["Mike Johnson", "40", "Chicago"],
        ]
    )
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue().encode("utf-8"),
            filename="people.csv",
        ),
    )


async def send_big_file(message: types.Message):
    # await asyncio.sleep(7)
    file = io.BytesIO()
    url = "https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result_bytes = await response.read()

    file.write(result_bytes)
    await message.reply_document(
        document=types.BufferedInputFile(
            # file=result_bytes,
            file=file.getvalue(),
            filename="cat-big-pic.jpeg",
        ),
    )


@dp.message(Command("pic_file"))
async def send_pic_file_buffered(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    # action_sender = ChatActionSender(
    #     bot=message.bot,
    #     chat_id=message.chat.id,
    #     action=ChatAction.UPLOAD_DOCUMENT,
    # )
    async with ChatActionSender.upload_document(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        await send_big_file(message)


# @dp.message(is_photo)
# @dp.message(lambda message: message.photo)
@dp.message(F.photo, ~F.caption)
async def handle_photo_wo_caption(message: types.Message):
    caption = "I can't see, sorry. Could you describe it please?"
    await message.reply_photo(
        photo=message.photo[-1].file_id,
        caption=caption,
    )


@dp.message(F.photo, F.caption.contains("please"))
async def handle_photo_with_please_caption(message: types.Message):
    await message.reply("Don't beg me. I can't see, sorry.")


any_media_filter = F.photo | F.video | F.document


@dp.message(any_media_filter, ~F.caption)
# @dp.message(F.photo, F.video, ~F.caption)
# @dp.message(F.photo | F.video | F.document, ~F.caption)
async def handle_any_media_wo_caption(message: types.Message):
    if message.document:
        await message.reply_document(
            document=message.document.file_id,
        )
    elif message.video:
        await message.reply_video(
            video=message.video.file_id,
        )
    else:
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

    if message.sticker:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.CHOOSE_STICKER,
        )
        # await asyncio.sleep(2)
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
