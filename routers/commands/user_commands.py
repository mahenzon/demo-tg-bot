import csv
import io

import aiohttp
from aiogram import Router, types
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender

from keyboards.inline_keyboards.actions_kb import build_actions_kb
from keyboards.inline_keyboards.shop_kb import build_shop_kb

router = Router(name=__name__)


@router.message(Command("code", prefix="/!%"))
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


@router.message(Command("pic"))
async def handle_command_pic(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    url = "https://t4.ftcdn.net/jpg/00/97/58/97/360_F_97589769_t45CqXyzjz0KXwoBZT9PRaWGHRk5hQqQ.jpg"
    await message.reply_photo(
        photo=url,
    )


@router.message(Command("file"))
async def handle_command_file(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    file_path = "/Users/suren/Downloads/cat.jpeg"
    await message.reply_document(
        document=types.FSInputFile(
            path=file_path,
            filename="cat-big-photo.jpeg",
        ),
    )


@router.message(Command("text"))
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


@router.message(Command("csv"))
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
    file = io.BytesIO()
    url = "https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result_bytes = await response.read()

    file.write(result_bytes)
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue(),
            filename="cat-big-pic.jpeg",
        ),
    )


@router.message(Command("pic_file"))
async def send_pic_file_buffered(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    async with ChatActionSender.upload_document(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        await send_big_file(message)


@router.message(Command("actions", prefix="!/"))
async def send_actions_message_w_kb(message: types.Message):
    await message.answer(
        text="Your actions:",
        reply_markup=build_actions_kb(),
    )


@router.message(Command("shop", prefix="!/"))
async def send_shop_message_kb(message: types.Message):
    await message.answer(
        text="Your shop actions:",
        reply_markup=build_shop_kb(),
    )
