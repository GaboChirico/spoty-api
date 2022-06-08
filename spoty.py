import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.cache_handler import CacheFileHandler

logger = logging.getLogger(__name__)
logging.basicConfig(filename='spotipy.log',
                    encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')

# Cache
cache_path = '.cache'
cache_handler = CacheFileHandler(cache_path=cache_path)
logger.info(cache_handler.get_cached_token())

# TEST ID's
logger.debug('Test Album: "0ZgTSm1VI55AhE09Nzvv11"')
logger.debug('Test Playlist: "37i9dQZF1DXagUeYbNSnOA"')


# Conexion con la API de Spotify.
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                                           client_secret=os.environ.get(
                                                               'SPOTIPY_CLIENT_SECRET'),
                                                           cache_handler=cache_handler))

# Meta y Features
meta = ['name', 'album', 'artists',
        'release_date', 'duration_ms', 'popularity']
features = ['danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness',
            'loudness', 'speechiness', 'key', 'mode', 'valence', 'tempo', 'time_signature']


def time_format(ms):
    """ Metodo de conversion de milisegundos a formato MM:SS """
    if int(ms) >= 3600000:  # Más de una hora
        return "{:02}:{:02}:{:02}".format(int((ms / 1000.0) / 3600), int((ms / 1000.0 / 60) % 60),
                                          int(ms / 1000.0 % 60))
    else:
        return "{:02}:{:02}".format(int((ms / 1000.0 / 60) % 60), int(ms / 1000.0 % 60))


def album_get_tracks_data(album_id):
    """ Metodo que genera la lista de ids de canciones por album """
    idList = [item['id'] for item in sp.album(album_id)['tracks']['items']]
    return [get_track_data(idList[item]) for item in range(len(idList))]


def playlist_get_tracks_data(playlist_id):
    """ Metodo que genera la lista de ids de canciones por playlist """
    idList = [item['track']['id']
              for item in sp.playlist(playlist_id)['tracks']['items']]
    return [get_track_data(idList[item]) for item in range(len(idList))]


def get_track_data(id):
    """ Metodo que obtiene los atributos de una cancion """
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


def get_album_data(album_id):
    """ Metodo que obtiene los atributos de un Album """
    get_data = sp.album(album_id)
    albumDict = {
        'Album': get_data['name'],
        'Artista': get_data['artists'][0]['name'],
        'Canciones': get_data['total_tracks'],
        'Duracion Total': time_format(sum([x['duration_ms'] for x in get_data['tracks']['items']])),
        'Lanzamiento': get_data['release_date'],
        'Popularidad': get_data['popularity'],
        'Album Label': get_data['label'],
        'Mercados': len(get_data['available_markets']),
        'Cover': get_data['images'][1]['url'],
    }
    return albumDict


def get_playlist_data(playlist_id):
    """ Metodo que obtiene los atributos de una playlist """
    get_data = sp.playlist(playlist_id)
    playlistDict = {
        'Playlist': get_data['name'],
        'Canciones': get_data['tracks']['total'],
        'Seguidores': get_data['followers']['total'],
        'Duracion Total': time_format(sum([x['track']['duration_ms'] for x in get_data['tracks']['items']])),
        'Popularidad Media': sum([x['track']['popularity'] for x in get_data['tracks']['items']]) / get_data['tracks']['total'],
        'Creador': get_data['owner']['display_name'],
        'Publica': (lambda x: 'Si' if x else 'No')(get_data['public']),
        'Colaboracion': (lambda x: 'Si' if x else 'No')(get_data['collaborative']),
        'Descripcion': get_data['description'],
        'Cover': get_data['images'][0]['url']
    }
    return playlistDict
