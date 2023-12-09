import logging


def get_logger(name):
    return logging.getLogger(name)


def setup_logger(name, level=logging.INFO):
    """Function setup as many loggers as you want"""
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s] - %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(stream_handler)

    return logger
