
# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL

from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Translation(object):

    # ============================================================
    # START
    # ============================================================

    START_TEXT = """👋 Hello <b>{}</b>

<blockquote>
I'm a Telegram URL Uploader Bot.
Send me a direct link and I'll upload it to Telegram
as a file or video.
</blockquote>

<b>Use the help button to learn how to use me!</b>
"""

    # ============================================================
    # HELP
    # ============================================================

    HELP_TEXT = """
<b>How To Use This Bot</b> 🤔

<blockquote>
• Go to /settings and customize the bot as you like.
• Send me a custom thumbnail to save it permanently.
• Send a link like this:
  https://example.com/file.mp4 | New Name.mkv
• Choose the desired upload option.
• Reply to any media with /caption + your text
  to set a caption.
</blockquote>
"""

    # ============================================================
    # ABOUT
    # ============================================================

    ABOUT_TEXT = """
╭───────────────⍟
│ 📛 <b>Bot Name</b> : URL Uploader Bot
│ 📢 <b>Framework</b> : <a href="https://docs.pyrogram.org/">PyroBlock 2.3.80</a>
│ 💻 <b>Language</b> : Python
│ 💾 <b>Database</b> : <a href="https://cloud.mongodb.com">MongoDB</a>
│ 🚨 <b>Support Group</b> : <a href="https://t.me/NT_BOTS_SUPPORT">NT Support</a>
│ 🥏 <b>Channel</b> : <a href="https://t.me/NT_BOT_CHANNEL">NT Bot Channel</a>
│ 👨‍💻 <b>Creator</b> : @NT_BOT_CHANNEL
╰───────────────⍟
"""

    # ============================================================
    # PROGRESS
    # ============================================================

    PROGRESS = """
┃ 📦 Progress : {0}%
┃ ✅ Done    : {1}
┃ 📁 Total   : {2}
┃ 🚀 Speed   : {3}/s
┃ 🕒 Time    : {4}
┗━━━━━━━━━━━━━━━━━━━━━
"""

    PROGRES = """
`{}`\n{}
"""

    # ============================================================
    # USER INFO
    # ============================================================

    INFO_TEXT = """
╭───────────────〄
│ 📛 First Name  : <b>{}</b>
│ 📛 Last Name   : <b>{}</b>
│ 👤 Username    : <b>@{}</b>
│ 🆔 Telegram ID : <code>{}</code>
│ 🖇️ Profile Link: <b>{}</b>
│ 📡 DC          : <b>{}</b>
│ 💮 Language    : <b>{}</b>
│ 💫 Status      : <b>{}</b>
╰──────────────────〄
"""

    # ============================================================
    # START BUTTONS
    # ============================================================

    START_BUTTONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🛠️ Settings",
                    callback_data="OpenSettings",
                    style=enums.ButtonStyle.SUCCESS,
                )
            ],
            [
                InlineKeyboardButton(
                    "🤝 Help",
                    callback_data="help",
                    style=enums.ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    "ℹ️ About",
                    callback_data="about",
                    style=enums.ButtonStyle.PRIMARY,
                ),
            ],
            [
                InlineKeyboardButton(
                    "✖️ Close",
                    callback_data="close",
                    style=enums.ButtonStyle.DANGER,
                )
            ],
        ]
    )

    # ============================================================
    # HELP BUTTONS
    # ============================================================

    HELP_BUTTONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🛠️ Settings",
                    callback_data="OpenSettings",
                    style=enums.ButtonStyle.SUCCESS,
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="home",
                    style=enums.ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    "ℹ️ About",
                    callback_data="about",
                    style=enums.ButtonStyle.PRIMARY,
                ),
            ],
            [
                InlineKeyboardButton(
                    "✖️ Close",
                    callback_data="close",
                    style=enums.ButtonStyle.DANGER,
                )
            ],
        ]
    )

    # ============================================================
    # ABOUT BUTTONS
    # ============================================================

    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🛠️ Settings",
                    callback_data="OpenSettings",
                    style=enums.ButtonStyle.SUCCESS,
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="home",
                    style=enums.ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    "🤝 Help",
                    callback_data="help",
                    style=enums.ButtonStyle.PRIMARY,
                ),
            ],
            [
                InlineKeyboardButton(
                    "✖️ Close",
                    callback_data="close",
                    style=enums.ButtonStyle.DANGER,
                )
            ],
        ]
    )

    # ============================================================
    # PLANS BUTTONS
    # ============================================================

    PLANS_BUTTONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ℹ️ About",
                    callback_data="about",
                    style=enums.ButtonStyle.SUCCESS,
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="home",
                    style=enums.ButtonStyle.PRIMARY,
                ),
                InlineKeyboardButton(
                    "🤝 Help",
                    callback_data="help",
                    style=enums.ButtonStyle.PRIMARY,
                ),
            ],
            [
                InlineKeyboardButton(
                    "✖️ Close",
                    callback_data="close",
                    style=enums.ButtonStyle.DANGER,
                )
            ],
        ]
    )

    # ============================================================
    # CLOSE BUTTON
    # ============================================================

    BUTTONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✖️ Close",
                    callback_data="close",
                    style=enums.ButtonStyle.DANGER,
                )
            ]
        ]
    )

    # ============================================================
    # GENERAL MESSAGES
    # ============================================================

    INCORRECT_REQUEST = "Error"

    DOWNLOAD_FAILED = "🔴 Error 🔴"

    TEXT = "Sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ"

    IFLONG_FILE_NAME = "Only 64 characters can be named."

    RENAME_403_ERR = (
        "Sorry. You are not permitted to rename this file."
    )

    ABS_TEXT = "Please don't be selfish."

    FORMAT_SELECTION = (
        "<b>Sᴇʟᴇᴄᴛ Yᴏᴜʀ Fᴏʀᴍᴀᴛ 👇</b>\n"
    )

    SET_CUSTOM_USERNAME_PASSWORD = """<b>🎥 Vɪᴅᴇᴏ = Uᴘʟᴏᴀᴅ As Sᴛʀᴇᴀᴍʙʟᴇ</b>

<b>📂 Fɪʟᴇ = Uᴘʟᴏᴀᴅ As Fɪʟᴇ</b>

<b>👮‍♂ Pᴏᴡᴇʀᴇᴅ Bʏ :</b> @NT_BOT_CHANNEL
"""

    DOWNLOAD_START = (
        "📥 Downloading... 📥\n\n"
        "File Name: {}"
    )

    UPLOAD_START = "📤 Uploading... 📤"

    # ============================================================
    # FILE SIZE / TELEGRAM LIMITS
    # ============================================================

    RCHD_BOT_API_LIMIT = (
        "Size greater than maximum allowed size (50MB). "
        "Nevertheless, trying to upload."
    )

    RCHD_TG_API_LIMIT = (
        "Downloaded in {} seconds.\n"
        "Detected File Size: {}\n\n"
        "Sorry, but I cannot upload files greater than "
        "the configured Telegram API limit.\n\n"
        "Use 4GB @UploaderXNTBot"
    )

    # ============================================================
    # SUCCESS
    # ============================================================

    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = (
        "**𝘛𝘏𝘈𝘕𝘒𝘚 𝘍𝘖𝘙 𝘜𝘚𝘐𝘕𝘎 𝘔𝘌** 🥰"
    )

    # ============================================================
    # THUMBNAIL
    # ============================================================

    SAVED_CUSTOM_THUMB_NAIL = (
        "🖼 Thumbnail saved permanently."
    )

    DEL_ETED_CUSTOM_THUMB_NAIL = (
        "🗑 Thumbnail deleted successfully."
    )

    # ============================================================
    # MEDIA
    # ============================================================

    FF_MPEG_DEL_ETED_CUSTOM_MEDIA = (
        "✅ Media cleared successfully."
    )

    CUSTOM_CAPTION_UL_FILE = " "

    NO_CUSTOM_THUMB_NAIL_FOUND = (
        "😅 No thumbnail found."
    )

    NO_VOID_FORMAT_FOUND = (
        "ERROR... <code>{}</code>"
    )

    FILE_NOT_FOUND = (
        "Error, File not Found!!"
    )

    # ============================================================
    # BOT ADVERTISEMENT
    # ============================================================

    FF_MPEG_RO_BOT_AD_VER_TISE_MENT = (
        "Join : @NT_BOT_CHANNEL\n"
        "For the list of Telegram bots."
    )

    # ============================================================
    # CAPTION HELP
    # ============================================================

    ADD_CAPTION_HELP = """Select an uploaded file/video or forward me
<b>Any Telegram File</b> and just write the text you want
to be on the file <b>as a reply to the file</b>.

The text you wrote will be attached as the caption! 🤩

Example:
<a href="https://te.legra.ph/file/ecf5297246c5fb574d1a0.jpg">
See This!
</a> 👇
"""
