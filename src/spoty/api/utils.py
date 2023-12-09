import json
import logging
import os
import time
from pathlib import Path

import pandas as pd
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyClientCredentials

from spoty.api.log import get_logger

LOGGER = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data"
if not Path(OUTPUT_DIR).exists():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


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
    return CacheFileHandler(cache_path=OUTPUT_DIR / "cache", username="Gabo")


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


def load_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)


def create_dataframe(
    data: object,
    meta: bool = True,
    features: bool = True,
    index: bool = True,
    ids: bool = True,
) -> pd.DataFrame:
    """
    Create pandas DataFrame from Album or Playlist object.

    Args:
        data (Album | Playlist): Album or Playlist object.
        meta (bool, optional): Enable meta data. Defaults to True.
        features (bool, optional): Enable feature data. Defaults to True.
        index (bool, optional): Enable index. Defaults to True.
        ids (bool, optional): Enable ids. Defaults to True.
    """

    df = pd.DataFrame([item.__dict__ for item in data.tracks])
    # Name dataframes
    df.Name = data.meta.name.replace(" ", "_")

    if not meta:
        df.drop(columns=META, inplace=True)
    if not features:
        df.drop(columns=FEATURES, inplace=True)
    if not ids:
        df.drop(columns="id", inplace=True)
    if not index:
        df.reset_index(drop=True, inplace=True)

    return df


def create_csv(df, output_dir=OUTPUT_DIR):
    if not Path(output_dir).exists():
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    try:
        df.to_csv(Path(output_dir) / f"{df.Name}.csv", sep=",", encoding="utf-8")
    except Exception as e:
        print(e)


def load_csv(file_path: str, sep: str = ",", encoding: str = "utf-8"):
    return pd.read_csv(file_path, sep=sep, encoding=encoding)


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
