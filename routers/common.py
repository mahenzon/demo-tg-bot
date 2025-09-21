from aiogram import F, Router, types
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage, ForwardMessage, CopyMessage
from aiogram.types import ReplyKeyboardRemove

from keyboards.common_keyboards import ButtonText

router = Router(name=__name__)


@router.message(F.text == ButtonText.BYE)
async def handle_bye_message(message: types.Message) -> SendMessage:
    return message.answer(
        text="See you later! Click /start any time!",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(
    message: types.Message,
    state: FSMContext,
) -> SendMessage:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return message.reply(text="OK, but nothing was going on.")

    await state.clear()
    return message.answer(
        f"Cancelled state {current_state}.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message()
async def echo_message(
    message: types.Message,
) -> ForwardMessage | SendMessage | CopyMessage:
    if message.poll:
        return message.forward(chat_id=message.chat.id)
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
        return message.copy_to(chat_id=message.chat.id)
    except TypeError:
        return message.reply(text="Something new 🙂")
