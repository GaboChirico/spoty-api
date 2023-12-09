from typing import List

from spoty.api.models.track import Track
from spoty.api.utils import time_format


class PlaylistMeta:
    def __init__(self, meta_data):
        self.name = meta_data["name"]
        self.length = meta_data["tracks"]["total"]
        self.followers = meta_data["followers"]["total"]
        self.total_duration = time_format(
            sum([x["track"]["duration_ms"] for x in meta_data["tracks"]["items"]])
        )
        self.average_popularity = round(
            sum([x["track"]["popularity"] for x in meta_data["tracks"]["items"]])
            / meta_data["tracks"]["total"],
            2,
        )
        self.owner = meta_data["owner"]["display_name"]
        self.public = (lambda x: "yes" if x else "no")(meta_data["public"])
        self.collaborative = (lambda x: "yes" if x else "no")(
            meta_data["collaborative"]
        )
        self.description = meta_data["description"]
        self.image_uri = meta_data["images"][0]["url"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


class Playlist:
    def __init__(self, id: str, tracks: List[Track], playlist_data):
        self.id = id
        self.tracks = tracks
        self.meta = PlaylistMeta(playlist_data)

    def serialize(self):
        return {
            "id": self.id,
            "tracks": [x.serialize() for x in self],
            "meta": self.meta.__dict__,
        }

    def __iter__(self):
        return iter(self.tracks)

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
    [Image] {self.meta.image_uri}
    """

    def __repr__(self) -> str:
        return f"Plyalist(id={self.id}, tracks={self.tracks}, playlist_data={self.playlist_data})"
