from .spoty import Spoty
from .models import Query
from .utils import LOGGER, check_env


def setup():
    check_env()
    LOGGER.info("Setup complete")


def main(query: str, type: str, limit: int = 50):
    LOGGER.info("Starting Spoty")
    setup()
    LOGGER.info("Creating query")
    query = Query(query, type, limit)
    LOGGER.info("Creating Spoty object")
    spoty = Spoty(query)
    LOGGER.info("Calling Spoty object")
    print(spoty())
    return spoty()
