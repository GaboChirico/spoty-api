from spoty import time_format


class Meta:

    def __init__(self, meta_data):
        self.name = meta_data['name']
        self.album = meta_data['album']['name']
        self.artists = meta_data['album']['artists'][0]['name']
        self.release_date = meta_data['album']['release_date']
        self.duration_ms = time_format(meta_data['duration_ms'])
        self.popularity = meta_data['popularity']


class Features:

    def __init__(self, feature_data):
        self.danceability = feature_data[0]['danceability']
        self.acousticness = feature_data[0]['acousticness']
        self.energy = feature_data[0]['energy']
        self.instrumentalness = feature_data[0]['instrumentalness']
        self.liveness = feature_data[0]['liveness']
        self.loudness = feature_data[0]['loudness']
        self.speechiness = feature_data[0]['speechiness']
        self.key = feature_data[0]['key']
        self.mode = feature_data[0]['mode']
        self.valence = feature_data[0]['valence']
        self.tempo = feature_data[0]['tempo']
        self.time_signature = feature_data[0]['time_signature']


class Track:

    def __init__(self, id: str, meta: Meta, features: Features):
        self.id = id
        self.meta = meta
        self.features = features

    def __str__(self) -> str:
        return f"{self.meta.name}"


class Album:

    def __init__(self, id: str, tracks: list[Track], album_data):
        self.id = id
        self.name = album_data['name']
        self.artist = album_data['artists'][0]['name']
        self.tracks = tracks
        self.total_tracks = album_data['total_tracks']
        self.total_duration = time_format(
            sum([x['duration_ms'] for x in album_data['tracks']['items']]))
        self.release_date = album_data['release_date']
        self.popularity = album_data['popularity']
        self.label = album_data['label']
        self.total_markets = len(album_data['available_markets'])
        self.image = album_data['images'][1]['url']

    def __str__(self) -> str:
        return f"Album: {self.name} by {self.artist}"


class Playlist:

    def __init__(self, id: str, tracks: list[Track], playlist_data):
        self.id = id
        self.name = playlist_data['name']
        self.tracks = tracks
        self.followers = playlist_data['followers']['total']
        self.total_duration = time_format(
            sum([x['track']['duration_ms'] for x in playlist_data['tracks']['items']]))
        self.average_popularity = sum(
            [x['track']['popularity'] for x in playlist_data['tracks']['items']]) / playlist_data['tracks']['total']
        self.owner = playlist_data['owner']['display_name']
        self.public = (lambda x: 'Yes' if x else 'No')(playlist_data['public'])
        self.collaborative = (lambda x: 'Yes' if x else 'No')(
            playlist_data['collaborative'])
        self.description = playlist_data['description']
        self.image = playlist_data['images'][0]['url']

    def __str__(self) -> str:
        return f"Playlist: {self.name} by {self.owner}"
