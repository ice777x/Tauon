from tauon.logger import logging
from tauon.core.client import Client
from tauon.config import API_HASH, API_ID, SESSION_STRING

HELP = {}


tauon = Client(
    name="tauon",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    workers=24,
    sleep_threshold=60,
)
