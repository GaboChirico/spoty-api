from collections.abc import Iterable
from typing import List

from spoty.api.models.track import Track
from spoty.api.utils import time_format


class AlbumMeta:
    def __init__(self, meta_data):
        self.name = meta_data["name"]
        self.artists = meta_data["artists"][0]["name"]
        self.release_date = meta_data["release_date"]
        self.total_tracks = meta_data["total_tracks"]
        self.popularity = meta_data["popularity"]
        self.total_duration = time_format(
            sum([x["duration_ms"] for x in meta_data["tracks"]["items"]])
        )
        self.label = meta_data["label"]
        self.total_markets = len(meta_data["available_markets"])
        self.image_uri = meta_data["images"][1]["url"]

    def __str__(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
        return ""


class Album:
    def __init__(self, id: str, tracks: List[Track], album_data):
        self.id = id
        self.tracks = tracks
        self.meta = AlbumMeta(album_data)

    def serialize(self):
        return {
            "id": self.id,
            "tracks": [x.serialize() for x in self],
            "meta": self.meta.__dict__,
        }

    def __str__(self) -> str:
        return f"""
    [Album] {self.meta.name}
    [Artists] {self.meta.artists}
    [Release Date] {self.meta.release_date} 
    [Total Tracks] {self.meta.total_tracks} 
    [Popularity] {self.meta.popularity}
    [Total Duration] {self.meta.total_duration} 
    [Label] {self.meta.label} 
    [Total Markets] {self.meta.total_markets}
    [Image] {self.meta.image_uri}]
"""

    def __iter__(self):
        return iter(self.tracks)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
