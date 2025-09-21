from aiogram import Router, F, types
from aiogram.enums import InputMediaType
from aiogram.methods import SendMessage, SendVideo, SendDocument
from aiogram.utils import markdown
from aiogram.utils.media_group import MediaGroupBuilder

from middlewares.album_middleware import AlbumMiddleware

router = Router(name=__name__)

any_media_filter = F.photo | F.video | F.document


router.message.middleware(AlbumMiddleware())


def get_media_file_id(m: types.Message) -> str:
    return m.video and m.video.file_id or m.photo[-1].file_id


@router.message(F.photo | F.video)
async def handle_media_group(
    message: types.Message,
    album_messages: list[types.Message] | None = None,
) -> SendMessage:
    if not album_messages:
        text = markdown.text(
            "Got media",
            markdown.hcode(
                get_media_file_id(message),
            ),
            "as a single item.",
            "",
            f"Has media group id: {markdown.hcode(message.media_group_id)}",
            sep="\n",
        )
        return message.reply(text=text)

    first_album_message = album_messages[0]
    text = markdown.text(
        f"New group of {len(album_messages)} messages received",
        markdown.text(
            *(
                f"{"🖼️" if m.photo else "🎥"} {markdown.hcode(get_media_file_id(m))}"
                for m in album_messages
            ),
            sep="\n",
        ),
        markdown.text(
            "as a media group with id",
            markdown.hcode(first_album_message.media_group_id),
        ),
        sep="\n\n",
    )
    await first_album_message.reply(text=text)
    builder = MediaGroupBuilder()
    for message in album_messages:
        builder.add(
            type=InputMediaType.VIDEO if message.video else InputMediaType.PHOTO,
            media=get_media_file_id(message),
            caption=message.caption,
            caption_entities=message.caption_entities,
            has_spoiler=message.has_media_spoiler,
            parse_mode=None,
        )

    media_group = builder.build()
    await first_album_message.reply_media_group(media_group)


@router.message(F.photo, F.caption.contains("please"))
async def handle_photo_with_please_caption(
    message: types.Message,
) -> SendMessage:
    return message.reply("Don't beg me. I can't see, sorry.")


@router.message(any_media_filter, ~F.caption)
async def handle_any_media_wo_caption(
    message: types.Message,
) -> SendMessage | SendVideo | SendDocument:
    if message.document:
        return message.reply_document(
            document=message.document.file_id,
        )

    if message.video:
        return message.reply_video(
            video=message.video.file_id,
        )

    return message.reply("I can't see.")


@router.message(any_media_filter, F.caption)
async def handle_any_media_w_caption(
    message: types.Message,
) -> SendMessage:
    return message.reply(f"Smth is on media. Your text: {message.caption!r}")
