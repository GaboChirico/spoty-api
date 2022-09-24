import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.cache_handler import CacheFileHandler
from spoty.models import Track, Meta, Features, Album, Playlist


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cache_path = BASE_DIR + 'tmp/.cache'
cache_handler = CacheFileHandler(cache_path=cache_path)\

logger = logging.getLogger(__name__)
logging.basicConfig(filename='tmp/spotipy.log',
                    encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')
logger.info(cache_handler.get_cached_token())
logger.debug('Test Album: "0ZgTSm1VI55AhE09Nzvv11"')
logger.debug('Test Playlist: "37i9dQZF1DXagUeYbNSnOA"')


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                                           client_secret=os.environ.get(
                                                               'SPOTIPY_CLIENT_SECRET'),
                                                           cache_handler=cache_handler))


def album_get_data(album_id: str):
    idList = [item['id'] for item in sp.album(album_id)['tracks']['items']]
    return Album(id=album_id, 
                 tracks=[get_track_data(idList[item]) for item in range(len(idList))], 
                 album_data=sp.album(album_id))


def playlist_get_tracks_data(playlist_id: str):
    idList = [item['track']['id']
              for item in sp.playlist(playlist_id)['tracks']['items']]
    return Playlist(id=playlist_id, 
                    tracks=[get_track_data(idList[item]) for item in range(len(idList))],
                    playlist_data=sp.playlist(playlist_id))


def get_track_data(id: str):
    return Track(id=id, meta=Meta(sp.track(id)), features=Features(sp.audio_features(id)))
