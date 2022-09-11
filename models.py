import dataclasses


@dataclasses.dataclass
class Meta:
    name: str
    album: str
    artists: str
    release_date: str
    duration_ms: float
    popularity: int


@dataclasses.dataclass
class Features:
    danceability: float
    acousticness: float
    energy: float
    instrumentalness: float
    liveness: float
    loudness: float
    speechiness: float
    key: int
    mode: int
    valence: float
    tempo: float
    time_signature: int


@dataclasses.dataclass
class Track:
    meta: Meta
    features: Features


class Album:
    def __init__(self, album_id: str):
        pass

    def __repr__(self):
        return f'Album({self.album_id})'

    def __str__(self) -> str:
        pass


class Playlist:
    def __init__(self, playlist_id: str):
        pass

    def __repr__(self):
        return f'Playlist({self.playlist_id})'

    def __str__(self) -> str:
        pass
