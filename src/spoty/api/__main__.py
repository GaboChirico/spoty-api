import logging

from spoty.api.core import Spoty
from spoty.api.utils import check_env
from spoty.api.log import setup_logger


def setup():
    check_env()
    setup_logger(__name__)
    logging.debug("Setup complete")


def search(
    query: str,
    type: str,
    limit: int = 50,
    features: bool = False,
):
    logging.info("Starting spoty...")
    setup()
    spoty = Spoty(query=query, type=type, limit=limit, features=features)
    logging.info("Processing search...")
    result = spoty.run()
    return result
