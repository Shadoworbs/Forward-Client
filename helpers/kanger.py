# (c) @AbirHasan2005

import asyncio
from configs import Config
from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram.errors import UserDeactivatedBan
from helpers.forwarder import ForwardMessage, ForwardAllMessages
from helpers.settings_manager import UserSettings


async def Kanger(c: Client, m: Message):
    # Get user settings
    user_settings = UserSettings(m.from_user.id)
    if not user_settings.has_required_settings():
        await m.edit(
            text="⚠️ Please configure your forwarding settings first using /settings"
        )
        return 400

    source_chats = user_settings.get_forward_from()
    destination_chats = user_settings.get_forward_to()

    await m.edit(
        text=f"🔍 Checking source chat(s) `{', '.join(map(str, source_chats))}` ..."
    )
    await asyncio.sleep(2)

    try:
        # Verify source chats
        for source_chat_id in source_chats:
            ForwardFromChat = await c.get_chat(chat_id=source_chat_id)
            await m.edit(
                text=f"✅ Successfully connected to source chat `{ForwardFromChat.title}`!"
            )
            await asyncio.sleep(1)
    except Exception as err:
        await m.edit(text=f"❌ Cannot access source chat!\n\n**Error:** `{err}`")
        return 400

    await asyncio.sleep(2)

    # Verify destination chats
    for chat_id in destination_chats:
        await m.edit(text=f"🔍 Checking destination chat `{chat_id}` ...")
        await asyncio.sleep(2)
        try:
            chat_member = await c.get_chat_member(
                chat_id=chat_id, user_id=(await c.get_me()).id
            )
            # if not chat_member.permissions.can_pin_messages:
            #     await m.edit(
            #         text=f"❌ No permission to send messages in chat `{chat_id}`!\nYou must be an admin with permission to send messages."
            #     )
            #     return 400
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
        # Use the new mass forwarding function for each source chat
        for source_chat_id in source_chats:
            success = await ForwardAllMessages(
                client=c,
                from_chat_id=source_chat_id,
                to_chat_ids=destination_chats,
            )

            if not success:
                await m.edit(
                    text=f"⚠️ Mass forward for chat {source_chat_id} completed with some errors."
                )
                await asyncio.sleep(2)

        await m.edit(text=f"✅ Mass forward completed successfully!\n\nBy: {(await c.get_me()).username}")

    except UserDeactivatedBan:
        await m.edit(text="❌ Account has been banned! Use an alternative account.")
    except Exception as err:
        await m.edit(text=f"❌ Mass forward failed!\n\n**Error:** `{err}`")
