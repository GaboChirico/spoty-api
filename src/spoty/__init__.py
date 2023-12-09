__version__ = "0.2.1"

from spoty.api.__main__ import search
from spoty.api.core import Spoty
from spoty.api.models.album import Album, AlbumMeta
from spoty.api.models.playlist import Playlist, PlaylistMeta
from spoty.api.models.query import Query
from spoty.api.models.track import AudioFeatures, Track, TrackMeta
from spoty.api.utils import (
    cache_handler,
    get_auth_token,
    spotify_credentials,
    time_format,
    track_time,
)

__all__ = [
    "search",
    "Spoty",
    "Album",
    "AlbumMeta",
    "Playlist",
    "PlaylistMeta",
    "Query",
    "AudioFeatures",
    "Track",
    "TrackMeta",
    "spotify_credentials",
    "time_format",
    "track_time",
    "cache_handler",
    "get_auth_token",
]
