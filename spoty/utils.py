import json
import os
import time
import logging
import pandas as pd
from spotipy.cache_handler import CacheFileHandler

# Logging
logging.basicConfig(filename='tmp/spotipy.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

# Cache handler
cache_handler = CacheFileHandler(cache_path=os.path.dirname(
    os.path.abspath(__file__)) + "tmp/.cache")


def load_json(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)


def create_csv(df):
    try:
        df.to_csv(df.name, sep=',', encoding='utf-8')
    except Exception as e:
        print(e)


def load_csv(file_name):
    return pd.read_csv(file_name, sep=',', encoding='utf-8')


def time_format(ms: float) -> str:
    """ 
    Time format miliseconds to MM:SS or HH:MM:SS

    Args:
        ms (float): miliseconds

    Returns:
        str: HH:MM:SS formated time.
    """
    if int(ms) >= 3600000:  # More than 1 hour
        return "{:02}:{:02}:{:02}".format(int((ms / 1000.0) / 3600), int((ms / 1000.0 / 60) % 60),
                                          int(ms / 1000.0 % 60))
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
