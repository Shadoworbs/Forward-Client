import asyncio
from typing import Optional, Union, List
from configs import Config
from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram.errors import (
    FloodWait,
    ChatWriteForbidden,
    UserBannedInChannel,
    ChatAdminRequired,
    MessageIdInvalid,
    MessageNotModified,
)
from helpers.filters import FilterMessage
from helpers.file_size_checker import CheckFileSize
from helpers.block_exts_handler import CheckBlockedExt


async def ForwardMessage(
    client: Client, msg: Message, silent: bool = False
) -> Union[int, bool]:
    """
    Forward a message to configured destination chats with advanced error handling and rate limiting

    Args:
        client: The Pyrogram client instance
        msg: The message to forward
        silent: If True, suppresses non-critical error messages

    Returns:
        400 on validation failure, True on success
    """
    try:
        # Skip validation for system messages and service notifications
        if msg.service or msg.empty:
            return True

        # --- Validation Checks --- #
        checks = [
            (FilterMessage(message=msg), "Message type not allowed in filters"),
            (
                CheckBlockedExt(event=msg) if msg.media else False,
                "File extension is blocked",
            ),
            (
                CheckFileSize(msg=msg) if msg.media else False,
                "File size below minimum requirement",
            ),
        ]

        for check_func, error_msg in checks:
            try:
                result = await check_func
                if isinstance(result, bool) and result is True:
                    if not silent:
                        await client.send_message(
                            "me", f"⚠️ Skipping message: {error_msg}"
                        )
                    return 400
                elif result == 400:
                    return 400
            except Exception as e:
                if not silent:
                    await client.send_message("me", f"⚠️ Validation error: {str(e)}")
                continue  # Skip this check if it fails

        # --- Forward to Each Chat --- #
        for chat_id in Config.FORWARD_TO_CHAT_ID:
            max_retries = 3
            retry_count = 0

            while retry_count < max_retries:
                try:
                    # Check permissions first
                    try:
                        chat = await client.get_chat(chat_id)
                        member = await chat.get_member("me")
                        if not member.can_send_messages:
                            await client.send_message(
                                chat_id="me",
                                text=f"⛔️ No permission to send messages in {chat.title}",
                            )
                            continue
                    except (ChatAdminRequired, UserBannedInChannel):
                        await client.send_message(
                            chat_id="me",
                            text=f"⛔️ Not allowed to send messages in chat {chat_id}",
                        )
                        continue

                    # Forward the message with progress tracking if media
                    try:
                        await msg.forward(chat_id=chat_id, disable_notification=True)
                        await asyncio.sleep(0.5)  # Small delay between forwards
                        break  # Success, exit retry loop
                    except MessageIdInvalid:
                        if not silent:
                            await client.send_message(
                                chat_id="me", text="⚠️ Message no longer available"
                            )
                        return 400

                except FloodWait as e:
                    if retry_count == max_retries - 1:
                        await client.send_message(
                            chat_id="me",
                            text=f"⚠️ FloodWait: Waiting {e.value} seconds for chat {chat_id}",
                        )
                        await asyncio.sleep(e.value)
                        retry_count += 1
                        continue
                    else:
                        await asyncio.sleep(e.value)
                        retry_count += 1
                        continue

                except Exception as e:
                    await client.send_message(
                        chat_id="me",
                        text=f"❌ Error forwarding to {chat_id}:\n`{str(e)}`",
                    )
                    break

        return True

    except Exception as e:
        await client.send_message(
            chat_id="me", text=f"❌ Unexpected error:\n`{str(e)}`"
        )
        return 400


async def ForwardAllMessages(
    client: Client, from_chat_id: int, to_chat_ids: List[int]
) -> bool:
    """
    Forward all messages from one chat to multiple destination chats, with chunking
    to avoid rate limits.

    Args:
        client: The Pyrogram client
        from_chat_id: Source chat ID
        to_chat_ids: List of destination chat IDs
    """
    try:
        chunk_size = 100
        messages_forwarded = 0
        failed_messages = 0

        # Get chat info for progress updates
        try:
            chat = await client.get_chat(from_chat_id)
            progress_message = await client.send_message(
                chat_id="me", text="🔄 Starting mass forward operation..."
            )
        except Exception as e:
            await client.send_message(
                chat_id="me", text=f"❌ Failed to get chat info: {str(e)}"
            )
            return False

        async for message in client.get_chat_history(from_chat_id):
            if messages_forwarded % chunk_size == 0:
                # Update progress every chunk
                await progress_message.edit_text(
                    f"📤 Forwarding messages from {chat.title}:\n"
                    f"✅ Forwarded: {messages_forwarded}\n"
                    f"❌ Failed: {failed_messages}"
                )
                await asyncio.sleep(2)  # Pause between chunks

            try:
                result = await ForwardMessage(client, message, silent=True)
                if result == 400:
                    failed_messages += 1
                else:
                    messages_forwarded += 1
            except Exception as e:
                failed_messages += 1
                continue

        # Final progress update
        await progress_message.edit_text(
            f"✅ Forward operation completed!\n\n"
            f"📊 Results from {chat.title}:\n"
            f"• Messages Forwarded: {messages_forwarded}\n"
            f"• Failed Messages: {failed_messages}"
        )
        return True

    except Exception as e:
        await client.send_message(
            chat_id="me", text=f"❌ Mass forward operation failed:\n`{str(e)}`"
        )
        return False
