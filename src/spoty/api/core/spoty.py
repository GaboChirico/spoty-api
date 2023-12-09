"""
Spoty API core Class
"""
import spotipy

from spoty.api.models import Album, AudioFeatures, Playlist, Query, Track, TrackMeta
from spoty.api.utils import spotify_credentials, track_time
from spoty.api.log import setup_logger

logger = setup_logger(__name__)


class Spoty:
    def __init__(
        self,
        query: str,
        type: str,
        limit: int = 50,
        features: bool = False,
    ):
        self.client = spotipy.Spotify(auth_manager=spotify_credentials())
        self.query = Query(
            query=query,
            type=type,
            limit=limit,
            features=features,
        )

    @track_time
    def run(self):
        self._valid_query()
        q = self.query.query
        match self.query.type:
            case "track":
                logger.info("Getting track %s." % q)
                return self.get_track(q)
            case "album":
                logger.info("Getting album %s." % q)
                return self.get_album(q)
            case "playlist":
                logger.info("Getting playlist %s." % q)
                return self.get_playlist(q)
            case _:
                raise ValueError("Invalid type")

    def _valid_query(self):
        try:
            self.client.search(q=self.query.query, type=self.query.type, limit=1)
            logger.info(f"Query: {self.query.query} is valid.")
        except Exception as e:
            logger.error(e)

    def get_album(self, album_id: str) -> Album:
        """
        Get album tracks and features.
        """
        return Album(
            id=album_id,
            tracks=[
                self.get_track(self.get_ids(album_id, type="album")[item])
                for item in range(len(self.get_ids(album_id, type="album")))
            ],
            album_data=self.client.album(album_id),
        )

    def get_playlist(self, playlist_id: str) -> Playlist:
        """
        Get playlist tracks and features.
        """
        return Playlist(
            id=playlist_id,
            tracks=[
                self.get_track(self.get_ids(playlist_id, type="playlist")[item])
                for item in range(len(self.get_ids(playlist_id, type="playlist")))
            ],
            playlist_data=self.client.playlist(playlist_id),
        )

    def get_ids(self, id, type: str) -> list[str]:
        """
        Get track IDs from album or playlist.
        """
        if type == "album":
            return [track["id"] for track in self.client.album_tracks(id)["items"]]
        elif type == "playlist":
            return [
                item["track"]["id"]
                for item in self.client.playlist(id)["tracks"]["items"]
            ]
        else:
            raise ValueError("Invalid type")

    def get_track(self, id: str) -> Track:
        """
        Get track meta and features.
        """
        if self.query.features:
            return Track(
                id=id,
                meta=TrackMeta(self.client.track(id)),
                features=AudioFeatures(self.client.audio_features(id)),
            )
        return Track(id=id, meta=TrackMeta(self.client.track(id)), features=None)

    def __str__(self) -> str:
        return f"{self.query.query: self.query.type}"

    def __repr__(self) -> str:
        return f"Soptify({self.query.query}, {self.query.type}, {self.query.limit})"
