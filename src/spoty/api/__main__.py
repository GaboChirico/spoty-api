from spoty.api.core import Spoty
from spoty.api.utils import LOGGER, check_env


def setup():
    check_env()
    LOGGER.debug("Setup complete")


def run(
    query: str,
    type: str,
    limit: int = 50,
    features: bool = False,
):
    LOGGER.info("Starting Spoty")
    setup()
    LOGGER.debug("Creating Spoty object")
    spoty = Spoty(query=query, type=type, limit=limit, features=features)
    LOGGER.info("Processing search...")
    result = spoty()
    LOGGER.info("Search complete")
    return result.serialize()
