"""
Utils module for the API
"""
import os
import time

from spotipy.cache_handler import CacheFileHandler, MemoryCacheHandler
from spotipy.oauth2 import SpotifyClientCredentials
from spoty.api.log import setup_logger

logger = setup_logger(__name__)


def cache_handler():
    """
    Check if cache file exists, if not use memory cache.
    """
    return (
        CacheFileHandler(cache_path=".cache")
        if os.path.exists(".cache")
        else MemoryCacheHandler()
    )


def get_auth_token():
    """
    Get cached token.
    """
    return cache_handler.get_cached_token()


def check_env():
    """
    Check if SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET are set.
    """
    if not os.environ.get("SPOTIPY_CLIENT_ID") and os.environ.get(
        "SPOTIPY_CLIENT_SECRET"
    ):
        logger.error(
            "Missing Credentials: Please set SPOTIPY_CLIENT_ID or SPOTIPY_CLIENT_SECRET"
        )


def spotify_credentials():
    """
    Get Spotify credentials.

    Returns:
        SpotifyClientCredentials: Spotify credentials.
    """
    return SpotifyClientCredentials(
        client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
        cache_handler=cache_handler(),
    )


def time_format(ms: float) -> str:
    """
    Time format miliseconds to MM:SS or HH:MM:SS

    Args:
        ms (float): miliseconds

    Returns:
        str: HH:MM:SS formated time.
    """
    if int(ms) >= 3600000:  # More than 1 hour
        return "{:02}:{:02}:{:02}".format(
            int((ms / 1000.0) / 3600),
            int((ms / 1000.0 / 60) % 60),
            int(ms / 1000.0 % 60),
        )
    else:
        return "{:02}:{:02}".format(int((ms / 1000.0 / 60) % 60), int(ms / 1000.0 % 60))


def track_time(func):
    """
    Decorator to track time elapsed in a function.
    """

    def wrapper(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        logger.info("Done. Took %s seconds." % (t2 - t1))
        return res

    return wrapper
