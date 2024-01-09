from aiogram import Router, F, types

router = Router(name=__name__)

any_media_filter = F.photo | F.video | F.document


@router.message(F.photo, ~F.caption)
async def handle_photo_wo_caption(message: types.Message):
    caption = "I can't see, sorry. Could you describe it please?"
    await message.reply_photo(
        photo=message.photo[-1].file_id,
        caption=caption,
    )


@router.message(F.photo, F.caption.contains("please"))
async def handle_photo_with_please_caption(message: types.Message):
    await message.reply("Don't beg me. I can't see, sorry.")


@router.message(any_media_filter, ~F.caption)
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


@router.message(any_media_filter, F.caption)
async def handle_any_media_w_caption(message: types.Message):
    await message.reply(f"Smth is on media. Your text: {message.caption!r}")
