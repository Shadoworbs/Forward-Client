# (c) @AbirHasan2005 | Thomas Shelby
# This is Telegram Messages Forwarder UserBot!
# Use this at your own risk. I will not be responsible for any kind of issue while using this!

from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config
from helpers.kanger import Kanger
from helpers.forwarder import ForwardMessage

RUN = {"isRunning": True}
User = Client(
    name="pyrogram",
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    in_memory=True,
    session_string=Config.STRING_SESSION,
)


@User.on_message(filters.text | filters.media)
async def main(client: Client, message: Message):
    if (-100 in Config.FORWARD_TO_CHAT_ID) or (-100 in Config.FORWARD_FROM_CHAT_ID):
        return

    if (message.text == "/start") and message.from_user.is_self:
        if not RUN["isRunning"]:
            RUN["isRunning"] = True
        await message.edit(
            text=f"Hi, **{message.from_user.first_name}**!\nThis is a Forwarder Userbot by @shadoworbs",
            disable_web_page_preview=True,
        )

    elif (message.text == "/stop") and message.from_user.is_self:
        RUN["isRunning"] = False
        return await message.edit(
            "Userbot Stopped!\n\nSend `/start` to start userbot again."
        )

    elif (message.text == "/help") and message.from_user.is_self and RUN["isRunning"]:
        await message.edit(text=Config.HELP_TEXT, disable_web_page_preview=True)

    elif (
        message.text
        and (message.text.startswith("/add_forward_to"))
        and message.from_user.is_self
        and RUN["isRunning"]
    ):
        if len(message.text.split(" ", 1)) < 2:
            return await message.edit(
                "Please give me Chat IDs to add in Forward To List!"
            )
        Config.FORWARD_TO_CHAT_ID.extend(
            [int(x) for x in message.text.split(" ", 1)[-1].split(" ")]
        )
        return await message.edit("Added Successfully!")

    elif (
        message.text
        and (message.text.startswith("/remove_forward_to"))
        and message.from_user.is_self
        and RUN["isRunning"]
    ):
        if len(message.text.split(" ", 1)) < 2:
            return await message.edit(
                "Please give me Chat IDs to remove from Forward To List!"
            )
        for x in message.text.split(" ", 1)[-1].split(" "):
            if int(x) in Config.FORWARD_TO_CHAT_ID:
                Config.FORWARD_TO_CHAT_ID.remove(int(x))
        return await message.edit("Removed Successfully!")

    elif (
        (message.text == "/forward") and message.from_user.is_self and RUN["isRunning"]
    ):
        await Kanger(c=client, m=message)

    elif message.chat.id in Config.FORWARD_FROM_CHAT_ID and RUN["isRunning"]:
        await ForwardMessage(client, message)


print("Bot running...")
User.run()
