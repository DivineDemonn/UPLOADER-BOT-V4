
import asyncio
import os
import random
import shutil
import string
import time

import psutil
from asyncio import TimeoutError

from pyrogram import Client, enums, errors, filters, types
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    CallbackQuery,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LinkPreviewOptions,
    Message,
)

from plugins.config import Config
from plugins.script import Translation
from plugins.database.add import AddUser
from plugins.database.database import db
from plugins.functions.forcesub import handle_force_subscribe
from plugins.functions.verify import check_token, verify_user
from plugins.settings.settings import OpenSettings


# ============================================================
# START COMMAND
# ============================================================

@Client.on_message(filters.private & filters.command("start"))
async def start(bot: Client, update: Message):
    # Force subscription
    if Config.UPDATES_CHANNEL is not None:
        fsub = await handle_force_subscribe(bot, update)

        if fsub == 400:
            return

    # Normal /start
    if len(update.command) != 2:
        await AddUser(bot, update)

        await update.reply_text(
            text=Translation.START_TEXT.format(
                update.from_user.mention
            ),
            reply_markup=Translation.START_BUTTONS,
            reply_to_message_id=update.id,
        )
        return

    # ========================================================
    # VERIFICATION LINK
    # ========================================================

    data = update.command[1]

    try:
        parts = data.split("-", 2)

        if len(parts) != 3 or parts[0] != "verify":
            return await update.reply_text(
                text="<b>Exᴘɪʀᴇᴅ Lɪɴᴋ Oʀ ⵊɴᴠᴀʟɪᴅ Lɪɴᴋ !</b>",
                protect_content=True,
                reply_to_message_id=update.id,
            )

        userid = parts[1]
        token = parts[2]

    except Exception:
        return await update.reply_text(
            text="<b>Exᴘɪʀᴇᴅ Lɪɴᴋ Oʀ ⵊɴᴠᴀʟɪᴅ Lɪɴᴋ !</b>",
            protect_content=True,
            reply_to_message_id=update.id,
        )

    # Check user ID
    if str(update.from_user.id) != str(userid):
        return await update.reply_text(
            text="<b>Exᴘɪʀᴇᴅ Lɪɴᴋ Oʀ ⵊɴᴠᴀʟɪᴅ Lɪɴᴋ !</b>",
            protect_content=True,
            reply_to_message_id=update.id,
        )

    # Validate token
    try:
        is_valid = await check_token(bot, userid, token)
    except Exception:
        is_valid = False

    if is_valid is True:
        await update.reply_text(
            text=(
                f"<b>Hᴇʏ {update.from_user.mention} 👋,\n"
                "ʏᴏᴜ Aʀᴇ Sᴜᴄᴄᴇssғᴜʟʟʏ Vᴇʀɪғɪᴇᴅ !\n\n"
                "Nᴏᴡ Yᴏᴜ Cᴀɴ Uᴘʟᴏᴀᴅ Fɪʟᴇs Aɴᴅ "
                "Vɪᴅᴇᴏs Tɪʟʟ Tᴏᴅᴀʏ Mɪᴅɴɪɢʜᴛ.</b>"
            ),
            protect_content=True,
            reply_to_message_id=update.id,
        )

        await verify_user(bot, userid, token)

    else:
        return await update.reply_text(
            text="<b>Exᴘɪʀᴇᴅ Lɪɴᴋ Oʀ ⵊɴᴠᴀʟɪᴅ Lɪɴᴋ !</b>",
            protect_content=True,
            reply_to_message_id=update.id,
        )


# ============================================================
# HELP
# ============================================================

@Client.on_message(
    filters.command("help", [".", "/"]) & filters.private
)
async def help_bot(bot: Client, m: Message):
    await AddUser(bot, m)

    return await m.reply_text(
        text=Translation.HELP_TEXT,
        reply_markup=Translation.HELP_BUTTONS,
        link_preview_options=LinkPreviewOptions(
            is_disabled=True
        ),
    )


# ============================================================
# ABOUT
# ============================================================

@Client.on_message(
    filters.command("about", [".", "/"]) & filters.private
)
async def aboutme(bot: Client, m: Message):
    await AddUser(bot, m)

    return await m.reply_text(
        text=Translation.ABOUT_TEXT,
        reply_markup=Translation.ABOUT_BUTTONS,
        link_preview_options=LinkPreviewOptions(
            is_disabled=True
        ),
    )


# ============================================================
# EDIT CAPTION
# ============================================================

@Client.on_message(
    filters.private & filters.reply & filters.text
)
async def edit_caption(bot: Client, update: Message):
    await AddUser(bot, update)

    replied = update.reply_to_message

    if not replied:
        return

    # Video
    if replied.video:
        try:
            await bot.send_cached_media(
                chat_id=update.chat.id,
                file_id=replied.video.file_id,
                caption=update.text,
            )
            return

        except Exception:
            pass

    # Document
    if replied.document:
        try:
            await bot.send_cached_media(
                chat_id=update.chat.id,
                file_id=replied.document.file_id,
                caption=update.text,
            )
            return

        except Exception:
            pass


# ============================================================
# CAPTION HELP
# ============================================================

@Client.on_message(
    filters.private
    & filters.command("caption", [".", "/"])
)
async def add_caption_help(bot: Client, update: Message):
    await AddUser(bot, update)

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ADD_CAPTION_HELP,
        reply_markup=Translation.BUTTONS,
    )


# ============================================================
# CANCEL DOWNLOAD
# ============================================================

@Client.on_callback_query(
    filters.regex(r"^cancel_download\+")
)
async def cancel_cb(c: Client, m: CallbackQuery):
    await m.answer()

    try:
        await m.message.edit_text("Trying to Cancel")
    except MessageNotModified:
        pass
    except Exception:
        return

    try:
        download_id = m.data.split("+", 1)[1]
    except (IndexError, AttributeError):
        try:
            await m.message.edit_text(
                "Invalid download ID."
            )
        except Exception:
            pass
        return

    # Check active download
    if download_id not in Config.DOWNLOAD_LOCATION:
        try:
            await m.message.edit_text(
                "This process is already cancelled. "
                "The bot may have been restarted."
            )
        except Exception:
            pass

        return

    # Remove download from active list
    try:
        Config.DOWNLOAD_LOCATION.remove(download_id)
    except ValueError:
        pass

    try:
        await m.message.edit_text(
            "✅ Download cancellation requested."
        )
    except Exception:
        pass


# ============================================================
# USER INFO
# ============================================================

@Client.on_message(
    filters.private & filters.command("info", [".", "/"])
)
async def info_handler(bot: Client, update: Message):

    user = update.from_user

    first_name = user.first_name or "None"
    last_name = user.last_name or "None"
    username = user.username or "None"
    user_id = user.id
    mention = user.mention

    dc_id = getattr(user, "dc_id", "Unknown")
    language_code = getattr(
        user,
        "language_code",
        "Unknown",
    )
    status = getattr(
        user,
        "status",
        "Unknown",
    )

    try:
        status = str(status)
    except Exception:
        status = "Unknown"

    await update.reply_text(
        text=Translation.INFO_TEXT.format(
            first_name,
            last_name,
            username,
            user_id,
            mention,
            dc_id,
            language_code,
            status,
        ),
        reply_markup=Translation.BUTTONS,
        link_preview_options=LinkPreviewOptions(
            is_disabled=True
        ),
    )


# ============================================================
# ADMIN WARNING
# ============================================================

@Client.on_message(
    filters.private & filters.command("warn")
)
async def warn(c: Client, m: Message):

    # Check user
    if not m.from_user:
        return

    # Check admin
    if m.from_user.id not in Config.ADMIN:
        await m.reply_text(
            text="You Are Not Admin 😡",
            quote=True,
        )
        return

    # Check arguments
    if len(m.command) < 3:
        await m.reply_text(
            "Usage:\n"
            "<code>/warn USER_ID REASON</code>"
        )
        return

    try:
        user_id = m.command[1]
        reason = m.text.split(" ", 2)[2]

        # Validate numeric Telegram ID
        user_id = int(user_id)

    except (ValueError, IndexError):
        await m.reply_text(
            "❌ Invalid user ID or missing reason."
        )
        return

    try:
        await c.send_message(
            chat_id=user_id,
            text=reason,
        )

        await m.reply_text(
            "✅ User Notified Successfully"
        )

    except Exception as e:
        await m.reply_text(
            "❌ User could not be notified."
        )
