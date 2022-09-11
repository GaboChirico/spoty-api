import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.cache_handler import CacheFileHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cache_path = BASE_DIR + '/.cache'
cache_handler = CacheFileHandler(cache_path=cache_path)\

logger = logging.getLogger(__name__)
logging.basicConfig(filename='spotipy.log',
                    encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')
logger.info(cache_handler.get_cached_token())
logger.debug('Test Album: "0ZgTSm1VI55AhE09Nzvv11"')
logger.debug('Test Playlist: "37i9dQZF1DXagUeYbNSnOA"')


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                                           client_secret=os.environ.get(
                                                               'SPOTIPY_CLIENT_SECRET'),
                                                           cache_handler=cache_handler))

meta = ['name', 'album', 'artists',
        'release_date', 'duration_ms', 'popularity']
features = ['danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness',
            'loudness', 'speechiness', 'key', 'mode', 'valence', 'tempo', 'time_signature']


def time_format(ms: float) -> str:
    """ 
    Time format miliseconds to MM:SS or HH:MM:SS

    Args:
        ms (float): miliseconds

    Returns:
        str: HH:MM:SS formated time.
    """
    if int(ms) >= 3600000:  # More than 1 hour
        return "{:02}:{:02}:{:02}".format(int((ms / 1000.0) / 3600), int((ms / 1000.0 / 60) % 60),
                                          int(ms / 1000.0 % 60))
    else:
        return "{:02}:{:02}".format(int((ms / 1000.0 / 60) % 60), int(ms / 1000.0 % 60))


def album_get_tracks_data(album_id: str):
    idList = [item['id'] for item in sp.album(album_id)['tracks']['items']]
    return [get_track_data(idList[item]) for item in range(len(idList))]


def playlist_get_tracks_data(playlist_id: str):
    idList = [item['track']['id']
              for item in sp.playlist(playlist_id)['tracks']['items']]
    return [get_track_data(idList[item]) for item in range(len(idList))]


def get_track_data(id: str):
    # meta
    get_meta = sp.track(id)
    name = get_meta['name']
    album = get_meta['album']['name']
    artist = get_meta['album']['artists'][0]['name']
    release_date = get_meta['album']['release_date']
    length = time_format(int(get_meta['duration_ms']))
    popularity = get_meta['popularity']

    # features
    get_features = sp.audio_features(id)
    danceability = get_features[0]['danceability']
    acousticness = get_features[0]['acousticness']
    energy = get_features[0]['energy']
    instrumentalness = get_features[0]['instrumentalness']
    liveness = get_features[0]['liveness']
    loudness = get_features[0]['loudness']
    speechiness = get_features[0]['speechiness']
    key = get_features[0]['key']
    mode = get_features[0]['mode']
    valence = get_features[0]['valence']
    tempo = get_features[0]['tempo']
    time_signature = get_features[0]['time_signature']

    return [name, album, artist, release_date, length, popularity, danceability, acousticness, energy,
            instrumentalness, liveness, loudness, speechiness, key, mode, valence, tempo, time_signature]


def get_album_data(album_id: str):
    # albumDict = {
    #     'Album': get_data['name'],
    #     'Artist': get_data['artists'][0]['name'],
    #     'Tracks': get_data['total_tracks'],
    #     'Total Duration': time_format(sum([x['duration_ms'] for x in get_data['tracks']['items']])),
    #     'Release': get_data['release_date'],
    #     'Popularity': get_data['popularity'],
    #     'Label': get_data['label'],
    #     'Markets': len(get_data['available_markets']),
    #     'Album Cover': get_data['images'][1]['url'],
    # }
    return sp.album(album_id)


def get_playlist_data(playlist_id: str):
    get_data = sp.playlist(playlist_id)
    # playlistDict = {
    #     'Playlist': get_data['name'],
    #     'Tracks': get_data['tracks']['total'],
    #     'Followers': get_data['followers']['total'],
    #     'Total Duration': time_format(sum([x['track']['duration_ms'] for x in get_data['tracks']['items']])),
    #     'Average Popularity': sum([x['track']['popularity'] for x in get_data['tracks']['items']]) / get_data['tracks']['total'],
    #     'Owner': get_data['owner']['display_name'],
    #     'Public': (lambda x: 'Yes' if x else 'No')(get_data['public']),
    #     'Collaborative': (lambda x: 'Yes' if x else 'No')(get_data['collaborative']),
    #     'Description': get_data['description'],
    #     'Playlist Cover': get_data['images'][0]['url']
    # }
    return sp.playlist(playlist_id)
