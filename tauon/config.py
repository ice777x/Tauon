from os import environ
from tauon import logging
from dotenv import load_dotenv
import heroku3

load_dotenv("config.env")

LOG = logging.addLevelName(1, levelName=__name__)

API_ID = environ.get("API_ID")
API_HASH = environ.get("API_HASH")

SESSION_STRING = environ.get("SESSION_STRING")

HEROKU_API_KEY = environ.get("HEROKU_API_KEY")
HEROKU_APP_NAME = environ.get("HEROKU_APP_NAME")
HERKOU_APP = (
    heroku3.from_key(HEROKU_API_KEY).apps()["HEROKU_APP_NAME"]
    if HEROKU_APP_NAME
    else None
)
