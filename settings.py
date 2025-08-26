from dotenv import load_dotenv
from os import getenv
# import os

load_dotenv()

# load_dotenv(dotenv_path=os.path.abspath(__file__))


class Settings:
    PATH_TO_DB = getenv(
        "PATH_TO_DB",
        default="sqlite:////home/YakomazovPavel/vaffelbot/vaffel.db",
    )
    TELEGRAM_BOT_TOKEN = getenv(
        "TELEGRAM_BOT_TOKEN",
        default="",
    )
    WEB_APP_URL = getenv(
        "PATH_TO_DB",
        default="",
    )
