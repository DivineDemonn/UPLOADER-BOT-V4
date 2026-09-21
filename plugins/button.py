# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL

import asyncio
import json
import logging
import os
import shutil
import time
from datetime import datetime

from pyrogram import enums
from pyrogram.types import InputMediaPhoto

from plugins.config import Config
from plugins.script import Translation
from plugins.thumbnail import *
from plugins.functions.display_progress import (
    progress_for_pyrogram,
    humanbytes,
)
from plugins.database.database import db
from plugins.functions.ran_text import random_char


# ============================================================
# Configuration
# ============================================================

COOKIES_FILE = "cookies.txt"


# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Reduce Pyrogram noise in production
logging.getLogger("pyrogram").setLevel(logging.WARNING)


# ============================================================
# Helper Functions
# ============================================================

def safe_remove(path: str):
    """Safely remove a file or directory."""
    if not path:
        return

    try:
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)

        elif os.path.isfile(path):
            os.remove(path)

    except Exception as error:
        logger.warning("Cleanup failed for %s: %s", path, error)


def get_url_from_message(message):
    """
    Extract URL from Telegram message entities.

    Supports:
    - text_link
    - url
    """
    if not message:
        return None

    text = message.text or message.caption or ""

    entities = message.entities or message.caption_entities or []

    for entity in entities:
        try:
            if entity.type == "text_link":
                return entity.url

            if entity.type == "url":
                offset = entity.offset
                length = entity.length
                return text[offset:offset + length]

        except Exception as error:
            logger.warning("URL extraction failed: %s", error)

    return text.strip() if text.strip() else None


def get_downloaded_file(path: str):
    """
    Find downloaded file.

    yt-dlp may produce the requested extension or MKV.
    """
    if os.path.isfile(path):
        return path

    base_path = os.path.splitext(path)[0]

    possible_extensions = (
        ".mkv",
        ".mp4",
        ".webm",
        ".mp3",
        ".m4a",
        ".opus",
        ".aac",
    )

    for extension in possible_extensions:
        candidate = base_path + extension

        if os.path.isfile(candidate):
            return candidate

    return None


# ============================================================
# YouTube Downloader Callback
# ============================================================

async def youtube_dl_call_back(bot, update):
    """
    Download YouTube media using yt-dlp and upload it to Telegram.
    """

    cb_data = update.data

    # --------------------------------------------------------
    # Parse callback data
    # --------------------------------------------------------

    try:
        tg_send_type, youtube_dl_format, youtube_dl_ext, ranom = cb_data.split(
            "|", 3
        )

    except ValueError:
        logger.error("Invalid callback data: %s", cb_data)

        try:
            await update.message.edit_caption(
                caption="❌ Invalid download request."
            )
        except Exception:
            pass

        return False

    random1 = random_char(5)

    user_id = update.from_user.id

    # --------------------------------------------------------
    # JSON metadata file
    # --------------------------------------------------------

    save_ytdl_json_path = os.path.join(
        Config.DOWNLOAD_LOCATION,
        f"{user_id}{ranom}.json",
    )

    try:
        with open(
            save_ytdl_json_path,
            "r",
            encoding="utf-8",
        ) as file:
            response_json = json.load(file)

    except FileNotFoundError:
        logger.error(
            "Download metadata file not found: %s",
            save_ytdl_json_path,
        )

        try:
            await update.message.delete()
        except Exception:
            pass

        return False

    except json.JSONDecodeError as error:
        logger.error(
            "Invalid JSON metadata file: %s",
            error,
        )

        try:
            await update.message.edit_caption(
                caption="❌ Download information is invalid. Please try again."
            )
        except Exception:
            pass

        safe_remove(save_ytdl_json_path)

        return False

    # --------------------------------------------------------
    # Get original URL/message
    # --------------------------------------------------------

    reply_message = update.message.reply_to_message

    if not reply_message:
        logger.error("Reply message not found.")

        try:
            await update.message.edit_caption(
                caption="❌ Original URL message was not found."
            )
        except Exception:
            pass

        safe_remove(save_ytdl_json_path)

        return False

    youtube_dl_url = (
        reply_message.text
        or reply_message.caption
        or ""
    ).strip()

    # --------------------------------------------------------
    # Default filename
    # --------------------------------------------------------

    title = response_json.get("title") or "download"

    custom_file_name = (
        f"{title}_{youtube_dl_format}.{youtube_dl_ext}"
    )

    youtube_dl_username = None
    youtube_dl_password = None

    # --------------------------------------------------------
    # Parse custom URL format
    #
    # URL
    #
    # URL|filename
    #
    # URL|filename|username|password
    # --------------------------------------------------------

    if "|" in youtube_dl_url:

        url_parts = youtube_dl_url.split("|")

        if len(url_parts) == 2:

            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]

        elif len(url_parts) == 4:

            (
                youtube_dl_url,
                custom_file_name,
                youtube_dl_username,
                youtube_dl_password,
            ) = url_parts

        else:

            extracted_url = get_url_from_message(reply_message)

            if extracted_url:
                youtube_dl_url = extracted_url

    else:

        extracted_url = get_url_from_message(reply_message)

        if extracted_url:
            youtube_dl_url = extracted_url

    youtube_dl_url = youtube_dl_url.strip()
    custom_file_name = custom_file_name.strip()

    if youtube_dl_username:
        youtube_dl_username = youtube_dl_username.strip()

    if youtube_dl_password:
        youtube_dl_password = youtube_dl_password.strip()

    logger.info(
        "Download requested by user %s",
        user_id,
    )

    logger.info(
        "URL: %s",
        youtube_dl_url,
    )

    logger.info(
        "Filename: %s",
        custom_file_name,
    )

    # --------------------------------------------------------
    # Validate URL
    # --------------------------------------------------------

    if not youtube_dl_url:
        try:
            await update.message.edit_caption(
                caption="❌ No valid URL was found."
            )
        except Exception:
            pass

        safe_remove(save_ytdl_json_path)

        return False

    # --------------------------------------------------------
    # Download started
    # --------------------------------------------------------

    try:
        await update.message.edit_caption(
            caption=Translation.DOWNLOAD_START.format(
                custom_file_name
            )
        )

    except Exception as error:
        logger.warning(
            "Unable to update download status: %s",
            error,
        )

    # --------------------------------------------------------
    # Description / caption
    # --------------------------------------------------------

    description = Translation.CUSTOM_CAPTION_UL_FILE

    if "fulltitle" in response_json:
        description = str(
            response_json["fulltitle"]
        )[:1021]

    # --------------------------------------------------------
    # User temporary directory
    # --------------------------------------------------------

    tmp_directory_for_each_user = os.path.join(
        Config.DOWNLOAD_LOCATION,
        f"{user_id}{random1}",
    )

    os.makedirs(
        tmp_directory_for_each_user,
        exist_ok=True,
    )

    download_directory = os.path.join(
        tmp_directory_for_each_user,
        custom_file_name,
    )

    # --------------------------------------------------------
    # yt-dlp command
    # --------------------------------------------------------

    if tg_send_type == "audio":

        command_to_exec = [
            "yt-dlp",

            "-c",

            "--max-filesize",
            str(Config.TG_MAX_FILE_SIZE),

            "--bidi-workaround",

            "--extract-audio",

            "--extractor-args",
            "youtube:player_client=web,web_embedded,tv",

            "--js-runtimes",
            "deno",

            "--remote-components",
            "ejs:github",

            "--cookies",
            COOKIES_FILE,

            "--audio-format",
            youtube_dl_ext,

            "--audio-quality",
            youtube_dl_format,

            youtube_dl_url,

            "-o",
            download_directory,
        ]

    else:

        command_to_exec = [
            "yt-dlp",

            "-c",

            "--max-filesize",
            str(Config.TG_MAX_FILE_SIZE),

            "--embed-subs",

            "--extractor-args",
            "youtube:player_client=web,web_embedded,tv",

            "--js-runtimes",
            "deno",

            "--remote-components",
            "ejs:github",

            "-f",
            f"{youtube_dl_format}/bestvideo+bestaudio/best",

            "--hls-prefer-ffmpeg",

            "--cookies",
            COOKIES_FILE,

            youtube_dl_url,

            "-o",
            download_directory,
        ]

    # --------------------------------------------------------
    # Optional HTTP proxy
    # --------------------------------------------------------

    if Config.HTTP_PROXY:
        command_to_exec.extend(
            [
                "--proxy",
                Config.HTTP_PROXY,
            ]
        )

    # --------------------------------------------------------
    # Optional authentication
    # --------------------------------------------------------

    if youtube_dl_username:
        command_to_exec.extend(
            [
                "--username",
                youtube_dl_username,
            ]
        )

    if youtube_dl_password:
        command_to_exec.extend(
            [
                "--password",
                youtube_dl_password,
            ]
        )

    # --------------------------------------------------------
    # yt-dlp final options
    # --------------------------------------------------------

    command_to_exec.extend(
        [
            "--no-warnings",
            "--newline",
        ]
    )

    logger.info(
        "Starting yt-dlp for user %s",
        user_id,
    )

    start = datetime.now()

    # --------------------------------------------------------
    # Start yt-dlp process
    # --------------------------------------------------------

    try:

        process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

    except FileNotFoundError:

        logger.exception(
            "yt-dlp executable was not found."
        )

        try:
            await update.message.edit_caption(
                caption=(
                    "❌ yt-dlp is not installed on the server."
                )
            )
        except Exception:
            pass

        safe_remove(tmp_directory_for_each_user)
        safe_remove(save_ytdl_json_path)

        return False

    except Exception as error:

        logger.exception(
            "Failed to start yt-dlp: %s",
            error,
        )

        try:
            await update.message.edit_caption(
                caption=f"❌ Downloader error: {error}"
            )
        except Exception:
            pass

        safe_remove(tmp_directory_for_each_user)
        safe_remove(save_ytdl_json_path)

        return False

    # --------------------------------------------------------
    # Decode process output
    # --------------------------------------------------------

    e_response = stderr.decode(
        "utf-8",
        errors="replace",
    ).strip()

    t_response = stdout.decode(
        "utf-8",
        errors="replace",
    ).strip()

    if e_response:
        logger.info(
            "yt-dlp stderr:\n%s",
            e_response[-5000:],
        )

    if t_response:
        logger.info(
            "yt-dlp stdout:\n%s",
            t_response[-5000:],
        )

    # --------------------------------------------------------
    # Download failed
    # --------------------------------------------------------

    if process.returncode != 0:

        logger.error(
            "yt-dlp failed with return code %s",
            process.returncode,
        )

        error_text = e_response or "Unknown yt-dlp error."

        # Avoid sending an enormous Telegram caption
        error_text = error_text[-3500:]

        try:
            await update.message.edit_caption(
                caption=f"❌ Download Error:\n\n{error_text}"
            )
        except Exception as error:
            logger.warning(
                "Unable to show download error: %s",
                error,
            )

        safe_remove(tmp_directory_for_each_user)
        safe_remove(save_ytdl_json_path)

        return False

    # --------------------------------------------------------
    # Handle invalid-link response
    # --------------------------------------------------------

    invalid_link_string = "**Invalid link !**"

    if (
        e_response
        and invalid_link_string in e_response
    ):

        error_message = e_response.replace(
            invalid_link_string,
            "",
        ).strip()

        try:
            await update.message.edit_caption(
                caption=error_message
            )
        except Exception:
            pass

        safe_remove(tmp_directory_for_each_user)
        safe_remove(save_ytdl_json_path)

        return False

    # --------------------------------------------------------
    # Check stdout
    # --------------------------------------------------------

    if not t_response:

        logger.error(
            "yt-dlp completed but returned no stdout."
        )

        try:
            await update.message.edit_caption(
                caption=Translation.DOWNLOAD_FAILED
            )
        except Exception:
            pass

        safe_remove(tmp_directory_for_each_user)
        safe_remove(save_ytdl_json_path)

        return False

    # --------------------------------------------------------
    # Remove JSON metadata
    # --------------------------------------------------------

    safe_remove(save_ytdl_json_path)

    # --------------------------------------------------------
    # Download timing
    # --------------------------------------------------------

    end_one = datetime.now()

    time_taken_for_download = int(
        (end_one - start).total_seconds()
    )

    # --------------------------------------------------------
    # Locate downloaded file
    # --------------------------------------------------------

    actual_downloaded_file = get_downloaded_file(
        download_directory
    )

    if not actual_downloaded_file:

        logger.error(
            "Downloaded file was not found: %s",
            download_directory,
        )

        try:
            await update.message.edit_caption(
                caption=Translation.DOWNLOAD_FAILED
            )
        except Exception:
            pass

        safe_remove(tmp_directory_for_each_user)

        return False

    download_directory = actual_downloaded_file

    file_size = os.path.getsize(
        download_directory
    )

    logger.info(
        "Downloaded file: %s",
        download_directory,
    )

    logger.info(
        "Downloaded size: %s",
        humanbytes(file_size),
    )

    # --------------------------------------------------------
    # Telegram maximum file size check
    # --------------------------------------------------------

    if file_size > Config.TG_MAX_FILE_SIZE:

        logger.warning(
            "File exceeds Telegram limit: %s",
            humanbytes(file_size),
        )

        try:
            await update.message.edit_caption(
                caption=Translation.RCHD_TG_API_LIMIT.format(
                    time_taken_for_download,
                    humanbytes(file_size),
                )
            )
        except Exception:
            pass

        safe_remove(tmp_directory_for_each_user)

        return False

    # --------------------------------------------------------
    # Upload started
    # --------------------------------------------------------

    try:
        await update.message.edit_caption(
            caption=Translation.UPLOAD_START.format(
                custom_file_name
            )
        )

    except Exception as error:
        logger.warning(
            "Unable to update upload status: %s",
            error,
        )

    start_time = time.time()

    thumbnail = None

    # --------------------------------------------------------
    # Upload media
    # --------------------------------------------------------

    try:

        # ====================================================
        # AUDIO
        # ====================================================

        if tg_send_type == "audio":

            duration = await Mdata03(
                download_directory
            )

            thumbnail = await Gthumb01(
                bot,
                update,
            )

            await update.message.reply_audio(
                audio=download_directory,
                caption=description,
                duration=duration,
                thumb=thumbnail,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    update.message,
                    start_time,
                ),
            )

        # ====================================================
        # VIDEO NOTE
        # ====================================================

        elif tg_send_type == "vm":

            width, duration = await Mdata02(
                download_directory
            )

            thumbnail = await Gthumb02(
                bot,
                update,
                duration,
                download_directory,
            )

            await update.message.reply_video_note(
                video_note=download_directory,
                duration=duration,
                length=width,
                thumb=thumbnail,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    update.message,
                    start_time,
                ),
            )

        # ====================================================
        # DOCUMENT / VIDEO
        # ====================================================

        else:

            upload_as_document = (
                await db.get_upload_as_doc(user_id)
            )

            if not upload_as_document:

                thumbnail = await Gthumb01(
                    bot,
                    update,
                )

                await update.message.reply_document(
                    document=download_directory,
                    thumb=thumbnail,
                    caption=description,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        start_time,
                    ),
                )

            else:

                width, height, duration = await Mdata01(
                    download_directory
                )

                thumbnail = await Gthumb02(
                    bot,
                    update,
                    duration,
                    download_directory,
                )

                await update.message.reply_video(
                    video=download_directory,
                    caption=description,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    thumb=thumbnail,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        start_time,
                    ),
                )

        logger.info(
            "Upload successful: %s",
            custom_file_name,
        )

    except Exception as error:

        logger.exception(
            "Upload failed for user %s: %s",
            user_id,
            error,
        )

        try:
            await update.message.edit_caption(
                caption=f"❌ Upload Error:\n\n{error}"
            )
        except Exception:
            pass

        safe_remove(tmp_directory_for_each_user)

        if thumbnail:
            safe_remove(thumbnail)

        return False

    # --------------------------------------------------------
    # Upload timing
    # --------------------------------------------------------

    end_two = datetime.now()

    time_taken_for_upload = int(
        (end_two - end_one).total_seconds()
    )

    # --------------------------------------------------------
    # Cleanup downloaded files
    # --------------------------------------------------------

    safe_remove(
        tmp_directory_for_each_user
    )

    if thumbnail:
        safe_remove(thumbnail)

    # --------------------------------------------------------
    # Final success message
    # --------------------------------------------------------

    try:

        await update.message.edit_caption(
            caption=(
                Translation
                .AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS
                .format(
                    time_taken_for_download,
                    time_taken_for_upload,
                )
            )
        )

    except Exception as error:

        logger.warning(
            "Unable to update final status: %s",
            error,
        )

    # --------------------------------------------------------
    # Final logs
    # --------------------------------------------------------

    logger.info(
        "✅ Download completed in %s seconds",
        time_taken_for_download,
    )

    logger.info(
        "✅ Upload completed in %s seconds",
        time_taken_for_upload,
    )

    logger.info(
        "✅ File completed: %s",
        custom_file_name,
    )

    return True
