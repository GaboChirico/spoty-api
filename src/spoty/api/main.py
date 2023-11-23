from spoty.api.core import Spoty
from spoty.api.models import Query
from spoty.api.utils import check_env, create_csv, create_dataframe, LOGGER


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
    return spoty()
