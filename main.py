# (c) @Shadoworbs | Shadoworbs
# This is Telegram Messages Forwarder UserBot!
# Use this at your own risk. I will not be responsible for any kind of issue while using this!

from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config
from helpers.kanger import Kanger
from helpers.forwarder import ForwardMessage
from helpers.settings_manager import UserSettings
from enum import Enum, auto
import time
from typing import Dict, Optional, Tuple
import asyncio


class InputState(Enum):
    FORWARD_FROM = auto()
    FORWARD_TO = auto()
    NONE = auto()


class UserState:
    def __init__(self, state: InputState = InputState.NONE):
        self.state = state
        self.timestamp = time.time()

    def is_expired(self, timeout_seconds: int = 300) -> bool:
        return (time.time() - self.timestamp) > timeout_seconds


# Dictionary to store user states
USER_STATES: Dict[int, UserState] = {}

RUN = {"isRunning": True}
WAITING_FOR = {}  # Store what kind of input we're waiting for from each user

User = Client(
    name="forwarder_userbot",
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    bot_token=Config.BOT_TOKEN,
)

# Dictionary to store user settings
user_settings_dict = {}


async def initialize_settings(user_id: int) -> UserSettings:
    """Initialize or get existing settings for a user"""
    if user_id not in user_settings_dict:
        settings = UserSettings(user_id)
        user_settings_dict[user_id] = settings
        # Update Config with user settings
        Config.FORWARD_FROM_CHAT_ID = settings.get_forward_from()
        Config.FORWARD_TO_CHAT_ID = settings.get_forward_to()
    return user_settings_dict[user_id]


async def handle_settings_prompt(message: Message, settings: UserSettings):
    """Handle settings prompts for users"""
    user_id = message.from_user.id

    if user_id in WAITING_FOR:
        prompt_type = WAITING_FOR[user_id]
        chat_id = message.text

        # Handle cancel command
        if chat_id.lower() == "cancel":
            del WAITING_FOR[user_id]
            await message.reply("❌ Settings update cancelled.")
            return

        # Validate the chat ID
        is_valid, cleaned_id = settings.validate_chat_id(chat_id)
        if not is_valid:
            await message.reply(
                "⚠️ Invalid chat ID format. Please send a valid chat ID or 'cancel' to stop."
            )
            return

        # Add the chat ID based on what we're waiting for
        if prompt_type == "forward_from":
            settings.add_forward_from(cleaned_id)
            remaining = "destination"
            next_prompt = "forward_to"
        else:  # forward_to
            settings.add_forward_to(cleaned_id)
            del WAITING_FOR[user_id]
            await message.reply(
                "✅ Settings have been updated successfully!\n\nUse /start to see available commands."
            )
            return

        # Update waiting state and send next prompt
        WAITING_FOR[user_id] = next_prompt
        await message.reply(
            f"✅ Source chat ID saved! Now send me the {remaining} chat ID or 'cancel' to stop."
        )
        return


def check_settings_text(settings: UserSettings):
    """Generate text to remind user about missing settings"""
    if not settings.has_required_settings():
        return "\n\n⚠️ Your forwarding settings are not configured. Use /settings to set them up."
    return ""


async def check_settings_required(message: Message, settings: UserSettings) -> bool:
    """Check if settings are configured and notify user if not"""
    if not settings.has_required_settings():
        await message.reply(
            "⚠️ You need to configure forwarding settings first!\n"
            "Use /settings or /bs to configure source and destination chats.\n\n"
            "Your original command will work once settings are configured."
        )
        return False
    return True


@User.on_message(filters.command(["start", "help"]))
async def start_command(client: Client, message: Message):
    """Handle start and help commands"""
    settings = await initialize_settings(message.from_user.id)

    # Add reset command to help text
    help_text = Config.HELP_TEXT.strip()
    help_text += "\n• `/rs` or `/reset` - Reset all forwarding settings."

    response = help_text
    if not settings.has_required_settings():
        response += "\n\n⚠️ Note: Please configure your forwarding settings using /settings or /bs first!"

    await message.reply(response)


@User.on_message(filters.command(["viewsettings", "vs"]))
async def view_settings(client: Client, message: Message):
    """Handle viewing settings command"""
    try:
        settings = await initialize_settings(message.from_user.id)

        if not settings.has_required_settings():
            await message.reply(
                "⚠️ No settings configured yet!\n\n"
                "Use /settings or /bs to configure your forwarding settings."
            )
            return

        # Get the settings
        forward_from = settings.get_forward_from()
        forward_to = settings.get_forward_to()

        # Format the settings nicely
        settings_text = "📋 **Current Forwarding Settings**\n\n"

        # Source chats section
        settings_text += "📤 **Source Chats:**\n"
        for i, chat_id in enumerate(forward_from, 1):
            settings_text += f"   {i}. `{chat_id}`\n"

        settings_text += "\n📥 **Destination Chats:**\n"
        for i, chat_id in enumerate(forward_to, 1):
            settings_text += f"   {i}. `{chat_id}`\n"

        settings_text += "\n⚙️ **Settings Summary:**\n"
        settings_text += (
            f"• Total Source Chats: {len(forward_from)}/{settings.MAX_CHATS}\n"
        )
        settings_text += (
            f"• Total Destination Chats: {len(forward_to)}/{settings.MAX_CHATS}\n"
        )
        settings_text += "\n💡 Use /settings to modify these configurations."

        await message.reply(settings_text)

    except Exception as e:
        await message.reply(
            "❌ An error occurred while retrieving settings!\n\n"
            f"Error details: `{str(e)}`\n"
            "Please try again or contact support if the issue persists."
        )


@User.on_message(filters.command(["settings", "bs", "botsettings"]))
async def settings_command(client: Client, message: Message):
    """Handle settings command"""
    user_id = message.from_user.id
    settings = await initialize_settings(user_id)

    state, is_expired = await get_user_state(user_id)

    if is_expired:
        await message.reply("Previous settings session expired. Starting new session.")

    if state != InputState.NONE:
        await message.reply(
            "You have a settings session in progress. Send '`cancel`' to start over."
        )
        return

    current_settings = (
        "Current Settings:\n"
        f"Source Chats: {', '.join(map(str, settings.get_forward_from()))}\n"
        f"Destination Chats: {', '.join(map(str, settings.get_forward_to()))}\n\n"
        "Send a source chat ID to start configuration, or '`cancel`' to exit."
    )

    await message.reply(current_settings)
    await set_user_state(user_id, InputState.FORWARD_FROM)


@User.on_message(filters.command(["kang", "stop"]))
async def handle_kang_stop(client: Client, message: Message):
    settings = await initialize_settings(message.from_user.id)

    if not settings.has_required_settings():
        await message.reply(
            "⚠️ You need to configure your forwarding settings first!\n"
            "Use /settings to set up the source and destination chats."
        )
        return

    # Continue with original command logic...
    if message.command[0].lower() == "kang":
        try:
            if RUN["isRunning"]:
                await message.edit_text("Already Running ...")
            else:
                RUN["isRunning"] = True
                await Kanger(c=client, m=message)
        except KeyboardInterrupt:
            await message.edit_text("Stopping Kang operation...")
            RUN["isRunning"] = False
    else:  # stop command
        RUN["isRunning"] = False
        await message.edit_text("Stopped Successfully!")


@User.on_message(filters.command(["rs", "reset"]))
async def reset_settings(client: Client, message: Message):
    """Handle reset settings command"""
    try:
        # Get user settings
        user_id = message.from_user.id
        settings = await initialize_settings(user_id)

        # Check if there are any settings to reset
        if not settings.has_required_settings():
            await message.reply("⚠️ No active settings found to reset!")
            return

        # Clear both forward from and to lists
        settings.clear_forward_from()
        settings.clear_forward_to()

        # Clear any active state
        await clear_user_state(user_id)

        await message.reply(
            "🗑️ Settings reset successfully!\n\n"
            "All forwarding configurations have been cleared. "
            "Use /settings or /bs to configure new settings."
        )
    except Exception as e:
        await message.reply(
            "❌ An error occurred while resetting settings!\n\n"
            f"Error details: {str(e)}\n"
            "Please try again or contact support if the issue persists."
        )


@User.on_message(
    ~filters.command(["start", "help", "settings", "bs", "botsettings", "kang", "stop"])
    & filters.text
)
async def handle_chat_id_input(client: Client, message: Message):
    """Handle chat ID input from users"""
    if not message.from_user:
        await message.reply("❌ Cannot process anonymous messages!")
        return

    user_id = message.from_user.id
    state, is_expired = await get_user_state(user_id)
    settings = await initialize_settings(user_id)

    if is_expired:
        await message.reply(
            "Settings session expired. Please use /settings to start over."
        )
        return

    if state == InputState.NONE:
        return

    chat_id = message.text.strip()
    validation_result = settings.validate_chat_id(chat_id)

    if not validation_result.is_valid:
        if validation_result.error_message == "Operation cancelled":
            await clear_user_state(user_id)
            await message.reply("Settings configuration cancelled.")
            return

        await message.reply(
            f"❌ {validation_result.error_message}\nPlease try again or send 'cancel' to exit."
        )
        return

    if state == InputState.FORWARD_FROM:
        success, msg = settings.add_forward_from(validation_result.cleaned_id)
        if success:
            await message.reply(
                f"{msg}\n\nNow send a destination chat ID, or 'cancel' to exit."
            )
            await set_user_state(user_id, InputState.FORWARD_TO)
        else:
            await message.reply(f"❌ {msg}\nPlease try again or send 'cancel' to exit.")

    elif state == InputState.FORWARD_TO:
        success, msg = settings.add_forward_to(validation_result.cleaned_id)
        if success:
            await clear_user_state(user_id)
            await message.reply(
                f"{msg}\n\n✅ Settings configured successfully!\n"
                "You can now use other commands like /kang"
            )
        else:
            await message.reply(f"❌ {msg}\nPlease try again or send 'cancel' to exit.")


@User.on_message(filters.command(["forward", "fwd"]))
async def forward_command(client: Client, message: Message):
    """Handle forward command - forwards a single message"""
    try:
        # Check for anonymous messages
        if not message.from_user:
            await message.reply("❌ Cannot process anonymous messages!")
            return

        # Initialize settings
        settings = await initialize_settings(message.from_user.id)

        # Check settings
        if not await check_settings_required(message, settings):
            return

        # Check if we have a replied-to message
        if not message.reply_to_message:
            await message.reply(
                "⚠️ Please reply to a message you want to forward with this command."
            )
            return

        await message.reply("🔄 Starting forward operation...")

        # Forward the message
        result = await ForwardMessage(client, message.reply_to_message)

        if result == 400:
            await message.reply(
                "❌ Failed to forward message. The message may:\n"
                "• Be filtered out by content type\n"
                "• Have a blocked file extension\n"
                "• Not meet minimum size requirements"
            )
        else:
            await message.reply("✅ Message forwarded successfully!")

    except Exception as e:
        await message.reply(
            "❌ Error occurred while forwarding:\n"
            f"`{str(e)}`\n"
            "Please try again or contact support if the issue persists."
        )


async def get_user_state(user_id: int) -> Tuple[InputState, bool]:
    """Get user's current state and whether it's expired"""
    if user_id not in USER_STATES:
        return InputState.NONE, False

    state = USER_STATES[user_id]
    is_expired = state.is_expired()

    if is_expired:
        USER_STATES.pop(user_id)
        return InputState.NONE, True

    return state.state, False


async def set_user_state(user_id: int, state: InputState):
    """Set user's current state"""
    USER_STATES[user_id] = UserState(state)


async def clear_user_state(user_id: int):
    """Clear user's current state"""
    if user_id in USER_STATES:
        USER_STATES.pop(user_id)


print("Bot running...")
User.run()
