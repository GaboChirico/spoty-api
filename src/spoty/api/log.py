"""
Log module for the API
"""

import logging


def setup_logger(name="spoty", level=logging.INFO) -> logging.Logger:
    """Function setup the logging module"""
    formatter = "[%(asctime)s][%(levelname)s] - %(message)s"
    log_level = logging.getLevelName(level)

    logging.basicConfig(level=log_level, format=formatter, datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(name)

    return logger
