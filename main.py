# (c) @AbirHasan2005 | Thomas Shelby
# This is Telegram Messages Forwarder UserBot!
# Use this at your own risk. I will not be responsible for any kind of issue while using this!

from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import FloodWait
from configs import Config
from helpers.kanger import Kanger
from helpers.forwarder import ForwardMessage
from helpers.settings_manager import UserSettings
from helpers.keyboard_manager import KeyboardManager

RUN = {"isRunning": True}
WAITING_FOR_INPUT = {}  # Store user states

User = Client(
    name="forwarder_userbot",
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    bot_token=Config.BOT_TOKEN,
)

# Initialize settings for current user
user_settings = None


async def initialize_settings(user_id: int):
    global user_settings
    user_settings = UserSettings(user_id)
    # Update Config with user settings
    Config.FORWARD_FROM_CHAT_ID = user_settings.get_forward_from()
    Config.FORWARD_TO_CHAT_ID = user_settings.get_forward_to()


@User.on_message(filters.text | filters.media)
async def main(client: Client, message: Message):
    global user_settings

    if not user_settings and message.from_user:
        await initialize_settings(message.from_user.id)

    if (-100 in Config.FORWARD_TO_CHAT_ID) or (-100 in Config.FORWARD_FROM_CHAT_ID):
        return

    if (message.text == "/start") and message.from_user.is_self:
        if not RUN["isRunning"]:
            RUN["isRunning"] = True
        await message.edit(
            text=f"Hi, **{message.from_user.first_name}**!\nThis is a Forwarder Userbot by @shadoworbs\n\nUse /bs or /botsettings to configure forwarding settings.",
            disable_web_page_preview=True,
        )

    elif (message.text in ["/bs", "/botsettings"]) and message.from_user.is_self:
        await message.edit(
            "🛠 **Bot Settings**\n\nUse the buttons below to configure forwarding settings:",
            reply_markup=KeyboardManager.settings_menu(),
        )

    elif (message.text == "/stop") and message.from_user.is_self:
        RUN["isRunning"] = False
        return await message.edit(
            "Userbot Stopped!\n\nSend `/start` to start userbot again."
        )

    elif (message.text == "/help") and message.from_user.is_self and RUN["isRunning"]:
        await message.edit(text=Config.HELP_TEXT, disable_web_page_preview=True)

    elif (
        (message.text == "/forward") and message.from_user.is_self and RUN["isRunning"]
    ):
        await Kanger(c=client, m=message)

    elif message.chat.id in Config.FORWARD_FROM_CHAT_ID and RUN["isRunning"]:
        await ForwardMessage(client, message)

    # Handle chat ID input when waiting for it
    elif (
        message.from_user.is_self
        and message.text
        and message.text.startswith("-100")
        and message.from_user.id in WAITING_FOR_INPUT
    ):
        input_type = WAITING_FOR_INPUT[message.from_user.id]
        chat_id = int(message.text)

        if input_type == "add_forward_from":
            success = user_settings.add_forward_from(chat_id)
            Config.FORWARD_FROM_CHAT_ID = user_settings.get_forward_from()
            await message.edit(
                f"✅ Forward from chat {'added' if success else 'already exists'}: `{chat_id}`",
                reply_markup=KeyboardManager.forward_from_menu(),
            )

        elif input_type == "add_forward_to":
            success = user_settings.add_forward_to(chat_id)
            Config.FORWARD_TO_CHAT_ID = user_settings.get_forward_to()
            await message.edit(
                f"✅ Forward to chat {'added' if success else 'already exists'}: `{chat_id}`",
                reply_markup=KeyboardManager.forward_to_menu(),
            )

        elif input_type == "remove_forward_from":
            success = user_settings.remove_forward_from(chat_id)
            Config.FORWARD_FROM_CHAT_ID = user_settings.get_forward_from()
            await message.edit(
                f"{'✅ Chat removed from forward from list' if success else '❌ Chat not found in forward from list'}: `{chat_id}`",
                reply_markup=KeyboardManager.forward_from_menu(),
            )

        elif input_type == "remove_forward_to":
            success = user_settings.remove_forward_to(chat_id)
            Config.FORWARD_TO_CHAT_ID = user_settings.get_forward_to()
            await message.edit(
                f"{'✅ Chat removed from forward to list' if success else '❌ Chat not found in forward to list'}: `{chat_id}`",
                reply_markup=KeyboardManager.forward_to_menu(),
            )

        del WAITING_FOR_INPUT[message.from_user.id]


@User.on_callback_query()
async def handle_callbacks(client: Client, callback: CallbackQuery):
    global user_settings

    if not user_settings and callback.from_user:
        await initialize_settings(callback.from_user.id)

    data = callback.data

    if data == "back_to_settings":
        await callback.message.edit(
            "🛠 **Bot Settings**\n\nUse the buttons below to configure forwarding settings:",
            reply_markup=KeyboardManager.settings_menu(),
        )

    elif data == "forward_from_menu":
        await callback.message.edit(
            "📥 **Forward From Settings**\n\nManage channels to forward messages from:",
            reply_markup=KeyboardManager.forward_from_menu(),
        )

    elif data == "forward_to_menu":
        await callback.message.edit(
            "📤 **Forward To Settings**\n\nManage channels to forward messages to:",
            reply_markup=KeyboardManager.forward_to_menu(),
        )

    elif data == "show_settings":
        from_chats = user_settings.get_forward_from()
        to_chats = user_settings.get_forward_to()

        settings_text = "**Current Settings**\n\n"
        settings_text += "📥 **Forward From:**\n"
        settings_text += (
            "\n".join([f"• `{chat_id}`" for chat_id in from_chats])
            if from_chats
            else "• None"
        )
        settings_text += "\n\n📤 **Forward To:**\n"
        settings_text += (
            "\n".join([f"• `{chat_id}`" for chat_id in to_chats])
            if to_chats
            else "• None"
        )

        await callback.message.edit(
            settings_text, reply_markup=KeyboardManager.settings_menu()
        )

    elif data in ["add_forward_from", "add_forward_to"]:
        WAITING_FOR_INPUT[callback.from_user.id] = data
        await callback.message.edit(
            "📝 Please send the chat ID (must start with -100):", reply_markup=None
        )

    elif data in ["remove_forward_from", "remove_forward_to"]:
        WAITING_FOR_INPUT[callback.from_user.id] = data
        await callback.message.edit(
            "📝 Please send the chat ID to remove (must start with -100):",
            reply_markup=None,
        )

    elif data == "clear_forward_from":
        user_settings.clear_forward_from()
        Config.FORWARD_FROM_CHAT_ID = []
        await callback.message.edit(
            "✅ Cleared all forward from channels",
            reply_markup=KeyboardManager.forward_from_menu(),
        )

    elif data == "clear_forward_to":
        user_settings.clear_forward_to()
        Config.FORWARD_TO_CHAT_ID = []
        await callback.message.edit(
            "✅ Cleared all forward to channels",
            reply_markup=KeyboardManager.forward_to_menu(),
        )

    elif data == "list_forward_from":
        chats = user_settings.get_forward_from()
        text = "📥 **Forward From Channels:**\n\n"
        text += (
            "\n".join([f"• `{chat_id}`" for chat_id in chats])
            if chats
            else "• No channels added"
        )
        await callback.message.edit(
            text, reply_markup=KeyboardManager.forward_from_menu()
        )

    elif data == "list_forward_to":
        chats = user_settings.get_forward_to()
        text = "📤 **Forward To Channels:**\n\n"
        text += (
            "\n".join([f"• `{chat_id}`" for chat_id in chats])
            if chats
            else "• No channels added"
        )
        await callback.message.edit(
            text, reply_markup=KeyboardManager.forward_to_menu()
        )


print("Bot running...")
User.run()
