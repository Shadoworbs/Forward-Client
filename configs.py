import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")


class Config(object):
    # Get This From @TeleORG_Bot
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    # Get This From @StringSessionGen_Bot
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    # Get This From @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

    # Filters for Forwards
    DEFAULT_FILTERS: str = os.environ.get("DEFAULT_FILTERS", "")
    FORWARD_FILTERS: str = os.environ.get("FORWARD_FILTERS", "")
    BLOCKED_EXTENSIONS = [x.strip() for x in os.environ.get("BLOCKED_EXTENSIONS", "")]
    MINIMUM_FILE_SIZE = os.environ.get("MINIMUM_FILE_SIZE", None)
    BLOCK_FILES_WITHOUT_EXTENSIONS = bool(
        os.environ.get("BLOCK_FILES_WITHOUT_EXTENSIONS", False)
    )
    # Forward as Copy. Value Should be True or False
    FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", False))
    # Sleep Time while Kang
    SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 10))
    # Message Texts
    HELP_TEXT = os.environ.get(
        "HELP_TEXT",
        """
This UserBot can forward messages from any Chat to any other Chat also you can kang all messages from one Chat to another Chat.

👨🏻‍💻 **Commands:**
• `/start` - Check UserBot Alive or Not.
• `/help` - Get this Message.
• `/kang` - Start All Messages Kanger.
• `/stop` - Stop Kanger & Restart Service.
• `/settings` - Configure forwarding settings.
• `/vs` - View current settings.
• `/rs` - Reset settings.
• `/forward` or `/fwd` - Forward a single message.

©️ **Developer:** @shadoworbs
👥 **Support Group:** [【★ʟя★】](https://t.me/pyrotestrobot)""",
    )
