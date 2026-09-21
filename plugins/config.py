import os
from os import environ, getenv
import logging

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO
)

class Config(object):
    
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8890692300:AAEpVvuVPPhlDYnmv8gVeZNE_3gANUF-LFI")
    API_ID = int(os.environ.get("API_ID", 24977986 ))
    API_HASH = os.environ.get("API_HASH", "abc6095228862c7502397c928bd7999e")
    
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    MAX_FILE_SIZE = 2194304000
    TG_MAX_FILE_SIZE = 2194304000
    FREE_USER_MAX_FILE_SIZE = 2194304000
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90")
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    
    OUO_IO_API_KEY = ""
    MAX_MESSAGE_LENGTH = 4096
    PROCESS_MAX_TIMEOUT = 3600
    DEF_WATER_MARK_FILE = "@Url_uploderbot"

    ADMIN = set(
        int(x) for x in environ.get("ADMIN", "").split()
        if x.isdigit()
    )

    BANNED_USERS = set(
        int(x) for x in environ.get("BANNED_USERS", "").split()
        if x.isdigit()
    )

    DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://VelouraMusic2002:VelouraMusic2002@velouramusic.p1yfjn6.mongodb.net/?appName=VelouraMusic")

    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1004468053767"))
    LOGGER = logging
    OWNER_ID = int(os.environ.get("OWNER_ID", "8885547727"))
    SESSION_NAME = "UploaderXNTBot"
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "-1004327295605")

    TG_MIN_FILE_SIZE = 2194304000
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "@Url_uploderbot")
    ADL_BOT_RQ = {}

    # Set False off else True
    TRUE_OR_FALSE = os.environ.get("TRUE_OR_FALSE", "").lower() == "true"

    # Shortlink settings
    SHORT_DOMAIN = environ.get("SHORT_DOMAIN", "")
    SHORT_API = environ.get("SHORT_API", "")

    # Verification video link
    VERIFICATION = os.environ.get("VERIFICATION", "")

    
