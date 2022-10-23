from .spoty import *
from .models import *
from .utils import *
from .entrypoint import *


def setup():
    check_env()
    LOGGER.info("Setup complete")


def spoty(query: str, type: str, limit: int = 50):
    LOGGER.info("Starting Spoty")
    setup()
    LOGGER.info("Creating query")
    query = Query(query, type, limit)
    LOGGER.info("Creating Spoty object")
    spoty = Spoty(query)
    LOGGER.info("Calling Spoty object")
    return spoty()
