import os
import time

from spotipy.cache_handler import CacheFileHandler, MemoryCacheHandler
from spotipy.oauth2 import SpotifyClientCredentials

from spoty.api.log import get_logger

LOGGER = get_logger(__name__)


META = ["name", "artists", "album", "duration_ms", "release_date", "popularity"]
FEATURES = [
    "danceability",
    "acousticness",
    "energy",
    "instrumentalness",
    "liveness",
    "loudness",
    "speechiness",
    "key",
    "mode",
    "valence",
    "tempo",
    "time_signature",
]

pitch_class_notation = {
    "0": "C",
    "1": "C#",
    "2": "D",
    "3": "D#",
    "4": "E",
    "5": "F",
    "6": "F#",
    "7": "G",
    "8": "G#",
    "9": "A",
    "10": "A#",
    "11": "B",
}


def cache_handler():
    return CacheFileHandler(cache_path=".cache") if os.path.exists(".cache") else MemoryCacheHandler()


def get_auth_token():
    return cache_handler.get_cached_token()


def check_env():
    if not os.environ.get("SPOTIPY_CLIENT_ID") and os.environ.get(
        "SPOTIPY_CLIENT_SECRET"
    ):
        LOGGER.error(
            "Missing Credentials: Please set SPOTIPY_CLIENT_ID or SPOTIPY_CLIENT_SECRET"
        )


def spotify_credentials():
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
    def wrapper(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        print(f"Time elapsed: {t2-t1} seconds")
        return res

    return wrapper
