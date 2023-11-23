from dataclasses import dataclass
from spoty.api.utils import time_format, pitch_class_notation


@dataclass
class Query:
    query: str
    type: str
    limit: int = 50


class Meta:
    def __init__(self, meta_data):
        self.name = meta_data["name"]
        self.album = meta_data["album"]["name"]
        self.artists = meta_data["album"]["artists"][0]["name"]
        self.release_date = meta_data["album"]["release_date"]
        self.duration_ms = time_format(meta_data["duration_ms"])
        self.popularity = meta_data["popularity"]


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
        self.image = meta_data["images"][1]["url"]

    def __str__(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
        return ""


class PlaylistMeta:
    def __init__(self, meta_data):
        self.name = meta_data["name"]
        self.followers = meta_data["followers"]["total"]
        self.total_duration = time_format(
            sum([x["track"]["duration_ms"] for x in meta_data["tracks"]["items"]])
        )
        self.average_popularity = (
            sum([x["track"]["popularity"] for x in meta_data["tracks"]["items"]])
            / meta_data["tracks"]["total"]
        )
        self.owner = meta_data["owner"]["display_name"]
        self.public = (lambda x: "Yes" if x else "No")(meta_data["public"])
        self.collaborative = (lambda x: "Yes" if x else "No")(
            meta_data["collaborative"]
        )
        self.description = meta_data["description"]
        self.image = meta_data["images"][0]["url"]


class Features:
    def __init__(self, feature_data):
        self.danceability = feature_data[0]["danceability"]
        self.acousticness = feature_data[0]["acousticness"]
        self.energy = feature_data[0]["energy"]
        self.instrumentalness = feature_data[0]["instrumentalness"]
        self.liveness = feature_data[0]["liveness"]
        self.loudness = feature_data[0]["loudness"]
        self.speechiness = feature_data[0]["speechiness"]
        self.key = (lambda x: pitch_class_notation[str(x)])(feature_data[0]["key"])
        self.mode = (lambda x: "major" if x == "1" else "minor")(
            feature_data[0]["mode"]
        )
        self.valence = feature_data[0]["valence"]
        self.tempo = feature_data[0]["tempo"]
        self.time_signature = feature_data[0]["time_signature"]
        self.valence = feature_data[0]["valence"]
        self.tempo = feature_data[0]["tempo"]
        self.time_signature = feature_data[0]["time_signature"]


class Track:
    def __init__(self, id: str, meta: Meta, features: Features):
        self.id = id
        for k, v in meta.__dict__.items():
            setattr(self, k, v)
        for k, v in features.__dict__.items():
            setattr(self, k, v)


class Album:
    def __init__(self, id: str, tracks: list[Track], album_data):
        self.id = id
        self.tracks = tracks
        self.meta = AlbumMeta(album_data)

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
    [Image] {self.meta.image}]
"""


class Playlist:
    def __init__(self, id: str, tracks: list[Track], playlist_data):
        self.id = id
        self.tracks = tracks
        self.meta = PlaylistMeta(playlist_data)

    def __str__(self) -> str:
        return f"""
    [Playlist] {self.meta.name}
    [Followers] {self.meta.followers}
    [Total Duration] {self.meta.total_duration}
    [Average Popularity] {self.meta.average_popularity}
    [Owner] {self.meta.owner}
    [Public] {self.meta.public}
    [Collaborative] {self.meta.collaborative}
    [Description] {self.meta.description}
    [Image] {self.meta.image}
"""
