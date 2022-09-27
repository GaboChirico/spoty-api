import os
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from models import Track, Meta, Features, Album, Playlist
from utils import logger, cache_handler, track_time


logger.info(cache_handler.get_cached_token())
logger.debug('Test Album: "0ZgTSm1VI55AhE09Nzvv11"')
logger.debug('Test Playlist: "37i9dQZF1DXagUeYbNSnOA"')


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                                           client_secret=os.environ.get(
                                                               'SPOTIPY_CLIENT_SECRET'),
                                                           cache_handler=cache_handler))


def get_id_list_from_album(album_id: str) -> list[str]:
    return [track['id'] for track in sp.album_tracks(album_id)['items']]


def get_id_list_from_playlist(playlist_id: str) -> list[str]:
    return [item['track']['id'] for item in sp.playlist(playlist_id)['tracks']['items']]


@track_time
def album_get_data(album_id: str) -> Album:
    return Album(id=album_id,
                 tracks=[get_track_data(get_id_list_from_album(album_id)[item])
                         for item in range(len(get_id_list_from_album(album_id)))],
                 album_data=sp.album(album_id))


@track_time
def playlist_get_data(playlist_id: str) -> Playlist:
    return Playlist(id=playlist_id,
                    tracks=[get_track_data(get_id_list_from_playlist(playlist_id)[item])
                            for item in range(len(get_id_list_from_playlist(playlist_id)))],
                    playlist_data=sp.playlist(playlist_id))


def get_track_data(id: str) -> Track:
    return Track(id=id, meta=Meta(sp.track(id)), features=Features(sp.audio_features(id)))


def create_dataframe(data: Playlist or Album,
                 meta: bool = True,
                 features: bool = True,
                 index: bool = True,
                 ids: bool = True) -> pd.DataFrame:

    df = pd.DataFrame([item.__dict__ for item in data.tracks])

    if not meta:
        df.drop(columns=['name', 'artists', 'album',
                'duration_ms', 'release_date', 'popularity'], inplace=True)

    if not features:
        df.drop(columns=['danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness',
                'loudness', 'speechiness', 'key', 'mode', 'valence', 'tempo', 'time_signature'], inplace=True)

    if not ids:
        df.drop(columns='id', inplace=True)

    if not index:
        df.reset_index(drop=True, inplace=True)

    return df


