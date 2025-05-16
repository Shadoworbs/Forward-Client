import os
import heroku3


class Config(object):
    # Get This From @TeleORG_Bot
    API_ID = int(os.environ.get("API_ID", '11518683'))
    API_HASH = os.environ.get("API_HASH", '100b7f1911bdb7d71a0bcde24e3408e6')
    # Get This From @StringSessionGen_Bot
    STRING_SESSION = os.environ.get("STRING_SESSION", 'BACvwtsAj1IDaCihcl6GFcM_wlHXlmeHjtXW2U_i7WS9smqRzJ-xhzjHXoFr2_D-cSC-OjZ61qVZfJnUJ8i0UsFwxAGkRiYKMOLZfIK_jhojJBxDqnoqD1BZ4La1HcyIMyHWsmuVhVfGBU2azOiClH58Z0DDo4hnbVJRAZWiGUAoLnDq4MZvuv0ZqKb63uy2Ve0w8EPHxK-uuhrIwo7w09D6LumU6OxC3wIpDFTOcaU-YN2sSDUnDMUUoApWyAMG3zRPeJzuJjCkpvYXUPhALBGMnlQ2SNEnpjr0lX6PvdWVoy0xiXP2JdZcohCUnuAsL-RRr0XzaNonFliix6bO1HzVrSLizQAAAABuhHWGAA')
    # Forward From Chat ID
    FORWARD_FROM_CHAT_ID = [-1001605270104,] #list(set(int(x) for x in os.environ.get("FORWARD_FROM_CHAT_ID", "-100").split()))
    # Forward To Chat ID
    FORWARD_TO_CHAT_ID = [-1001711685518,] #list(set(int(x) for x in os.environ.get("FORWARD_TO_CHAT_ID", "-100").split()))
    # Filters for Forwards
    DEFAULT_FILTERS = 'video document' #"video document photo audio text gif forwarded poll sticker"
    FORWARD_FILTERS = list(set(x for x in os.environ.get("FORWARD_FILTERS", DEFAULT_FILTERS).split()))
    BLOCKED_EXTENSIONS = ['rar', 'zip', 'txt', 'iso', 'ziv', 'apk', 'exe', 'torrent'] #list(set(x for x in os.environ.get("BLOCKED_EXTENSIONS", "").split()))
    MINIMUM_FILE_SIZE = os.environ.get("MINIMUM_FILE_SIZE", None)
    BLOCK_FILES_WITHOUT_EXTENSIONS = bool(os.environ.get("BLOCK_FILES_WITHOUT_EXTENSIONS", False))
    # Forward as Copy. Value Should be True or False
    FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", False))
    # Sleep Time while Kang
    SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 10))
    # Heroku Management
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    HEROKU_APP = heroku3.from_key(HEROKU_API_KEY).apps()[HEROKU_APP_NAME] if HEROKU_API_KEY and HEROKU_APP_NAME else None
    # Message Texts
    HELP_TEXT = """
This UserBot can forward messages from any Chat to any other Chat also you can kang all messages from one Chat to another Chat.

👨🏻‍💻 **Commands:**
• `/start` - Check UserBot Alive or Not.
• `/help` - Get this Message.
• `/kang` - Start All Messages Kanger.
• `/restart` - Restart Heroku App Dyno Workers.
• `/stop` - Stop Kanger & Restart Service.

©️ **Developer:** @shadoworbs
👥 **Support Group:** [【★ʟя★】](https://t.me/pyrotestrobot)"""
