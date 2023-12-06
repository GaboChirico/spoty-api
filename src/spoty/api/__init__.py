__version__ = "0.2.0"

from spoty.api.core import Spoty
from spoty.api.models.album import Album, AlbumMeta
from spoty.api.models.playlist import Playlist, PlaylistMeta
from spoty.api.models.query import Query
from spoty.api.models.track import AudioFeatures, Track, TrackMeta
from spoty.api.utils import spotify_credentials, time_format, track_time

__all__ = [
    "Spoty",
    "Album",
    "AlbumMeta",
    "Playlist",
    "PlaylistMeta",
    "Track",
    "AudioFeatures",
    "TrackMeta",
    "Query",
    "spotify_credentials",
    "track_time",
    "time_format",
]

__author__ = "Gabriel Chirico"
