from spoty.api.constants import PCN
from spoty.api.utils import time_format


class TrackMeta:
    def __init__(self, meta_data):
        self.name = meta_data["name"]
        self.album = meta_data["album"]["name"]
        self.artists = meta_data["album"]["artists"][0]["name"]
        self.release_date = meta_data["album"]["release_date"]
        self.duration_ms = time_format(meta_data["duration_ms"])
        self.popularity = meta_data["popularity"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __str__(self) -> str:
        return f"""
    [Track] {self.name}
    [Album] {self.album}
    [Artists] {self.artists}
    [Release Date] {self.release_date}
    [Duration] {self.duration_ms}
    [Popularity] {self.popularity}
    """


class AudioFeatures:
    def __init__(self, feature_data):
        self.danceability = feature_data[0]["danceability"]
        self.acousticness = feature_data[0]["acousticness"]
        self.energy = feature_data[0]["energy"]
        self.instrumentalness = feature_data[0]["instrumentalness"]
        self.liveness = feature_data[0]["liveness"]
        self.loudness = feature_data[0]["loudness"]
        self.speechiness = feature_data[0]["speechiness"]
        self.key = (lambda x: PCN[str(x)])(feature_data[0]["key"])
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
    def __init__(self, id: str, meta: TrackMeta, features: AudioFeatures):
        self.id = id
        self.meta = meta
        self.features = features
        for k, v in meta.__dict__.items():
            setattr(self, k, v)
        if features:
            for k, v in features.__dict__.items():
                setattr(self, k, v)

    def serialize(self):
        if self.features:
            return {
                "id": self.id,
                "meta": self.meta.__dict__,
                "features": self.features.__dict__,
            }
        return {
            "id": self.id,
            "meta": self.meta.__dict__,
        }

    def __str__(self) -> str:
        return f"""
    [Track] {self.name}
    [Artists] {self.artists}
    """

    def __repr__(self) -> str:
        return f"Track(id={self.id}, meta={self.meta}, features={self.features})"
