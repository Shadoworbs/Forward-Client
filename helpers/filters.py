# (c) @Shadoworbs

from configs import Config
from pyrogram.types import Message


async def FilterMessage(message: Message):
    # Using new forward_origin properties
    has_forward = bool(
        message.forward_origin
        and (message.forward_origin.sender_user or message.forward_origin.sender_chat)
    )
    if has_forward and ("forwarded" not in Config.FORWARD_FILTERS):
        return 400

    # Rest of the filters
    if (len(Config.FORWARD_FILTERS.lower()) == "all") or (
        (message.video and ("video" in Config.FORWARD_FILTERS))
        or (message.document and ("document" in Config.FORWARD_FILTERS))
        or (message.photo and ("photo" in Config.FORWARD_FILTERS))
        or (message.audio and ("audio" in Config.FORWARD_FILTERS))
        or (message.text and ("text" in Config.FORWARD_FILTERS))
        or (message.animation and ("gif" in Config.FORWARD_FILTERS))
        or (message.poll and ("poll" in Config.FORWARD_FILTERS))
        or (message.sticker and ("sticker" in Config.FORWARD_FILTERS))
    ):
        return 200
    else:
        return 400
