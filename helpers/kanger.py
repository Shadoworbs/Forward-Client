# (c) @AbirHasan2005

import asyncio
from configs import Config
from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram.errors import UserDeactivatedBan
from helpers.forwarder import ForwardMessage, ForwardAllMessages


async def Kanger(c: Client, m: Message):
    await m.edit(
        text=f"🔍 Checking source chat `{str(Config.FORWARD_FROM_CHAT_ID)}` ..."
    )
    await asyncio.sleep(2)

    try:
        # Verify source chat
        ForwardFromChat = await c.get_chat(chat_id=Config.FORWARD_FROM_CHAT_ID)
        await m.edit(
            text=f"✅ Successfully connected to source chat `{ForwardFromChat.title}`!"
        )
    except Exception as err:
        await m.edit(text=f"❌ Cannot access source chat!\n\n**Error:** `{err}`")
        return 400

    await asyncio.sleep(2)

    # Verify destination chats
    for chat_id in Config.FORWARD_TO_CHAT_ID:
        await m.edit(text=f"🔍 Checking destination chat `{chat_id}` ...")
        await asyncio.sleep(2)
        try:
            chat_member = await c.get_chat_member(
                chat_id=chat_id, user_id=(await c.get_me()).id
            )
            if not chat_member.can_send_messages:
                await m.edit(
                    text=f"❌ No permission to send messages in chat `{chat_id}`!"
                )
                return 400
            chat = await c.get_chat(chat_id)
            await m.edit(
                text=f"✅ Successfully connected to destination chat `{chat.title}`!"
            )
            await asyncio.sleep(2)
        except Exception as err:
            await m.edit(
                text=f"❌ Cannot access destination chat!\n\n**Error:** `{err}`"
            )
            return 400

    await m.edit(text="🚀 Starting mass forward operation...")

    try:
        # Use the new mass forwarding function
        success = await ForwardAllMessages(
            client=c,
            from_chat_id=Config.FORWARD_FROM_CHAT_ID[0],
            to_chat_ids=Config.FORWARD_TO_CHAT_ID,
        )

        if success:
            await m.edit(text="✅ Mass forward completed successfully!")
        else:
            await m.edit(text="⚠️ Mass forward completed with some errors.")

    except UserDeactivatedBan:
        await m.edit(text="❌ Account has been banned! Use an alternative account.")
    except Exception as err:
        await m.edit(text=f"❌ Mass forward failed!\n\n**Error:** `{err}`")
