# Forward-Client
This is Telegram Messages Forwarder bot by [@shadoworbs](https://github.com/Shadoworbs).

Use this at your own risk. I will not be responsible for any kind of issue while using this! Better use a different Telegram Account instead of using Main Telegram Account.

### Features:
- Forward Whole Chat Messages to other Chats.
    - Can cause Telegram Account Ban!
- Forward From Chat To Chat.
    - Can Forward from Multiple Chats to Multiple Chats
    - Automatically forward new messages From Chat To Chat.
- Bot
- Simple & Userfriendly

### Configs:
- `API_ID` - Get from my.telegram.org
- `API_HASH` - Get from my.telegram.org
- `STRING_SESSION` - Generate a pyrogram session from [Session String Generator](https://colab.research.google.com/drive/1wjYvtwUo5zDsUvukyafAR9Of-2NYkKsu)
- `FORWARD_FILTERS` - Filters can be `text`, `video`, `document`, `gif`, `sticker`, `photo`, `audio`, `poll`, `forwarded`. Separate with Space.
- `FORWARD_TO_CHAT_ID` - Forward To Chat IDs. Separate with Space.
- `FORWARD_FROM_CHAT_ID` - Forward From Chat IDs. Separate with Space.
- `FORWARD_AS_COPY` - Forward Messages as Copy or with Forward Tag. Value should be `True`/`False`.
- `BLOCKED_EXTENSIONS` - Don't Forward those Media Messages which contains Blocked Extensions. Example: `mp4 mkv mp3 zip rar`. Separate with Space.
- `MINIMUM_FILE_SIZE` - Minimum File Size for Media Message to be able to Forward. Should be in Bytes.
- `BLOCK_FILES_WITHOUT_EXTENSIONS` - Value can be `True`/`False`. If `True` those files which doesn't have file extension will not be Forwarded.

### **Commands:**
- `/start` - Check Bot Alive or Not.
- `/help` - Get this Message.
- `/kang` - Start All Messages Kanger.
- `/restart` - Restart Heroku App Dyno Workers.
- `/stop` - Stop Kanger & Restart Service.

### Support Group:
<a href="https://t.me/pyrotestrobot"><img src="https://img.shields.io/badge/Telegram-Join%20Telegram%20Group-blue.svg?logo=telegram"></a>

### Video Tutorial:
[![YouTube](https://img.shields.io/badge/YouTube-Video%20Tutorial-red?logo=youtube)](https://youtu.be/_xuptk2KUbk)

### Deploy Now:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AbirHasan2005/Forward-Client)

### Host Locally:
```sh
git clone https://github.com/AbirHasan2005/Forward-Client
cd Forward-Client
pip3 install -r requirements.txt
# Setup Configurations in configs.py file!
python3 main.py
```

### Follow on:
<p align="left">
<a href="https://github.com/shadoworbs"><img src="https://img.shields.io/badge/GitHub-Follow%20on%20GitHub-inactive.svg?logo=github"></a>
<!-- </p>
<p align="left">
<a href="https://twitter.com/shadoworbs123"><img src="https://img.shields.io/badge/Twitter-Follow%20on%20Twitter-informational.svg?logo=twitter"></a>
</p>
<p align="left">
<a href="https://facebook.com/shadoworbs/1"><img src="https://img.shields.io/badge/Facebook-Follow%20on%20Facebook-blue.svg?logo=facebook"></a>
</p>
<p align="left">
<a href="https://instagram.com/shadoworbs123"><img src="https://img.shields.io/badge/Instagram-Follow%20on%20Instagram-important.svg?logo=instagram"></a>
</p> -->
