import json 

from spoty.api import models
from spoty.api import utils


class Serialize():
    def __init__(self, data):
        self.data = data
        
    def serialize(self):
        pass
    
    def deserialize(self):
        pass
    
    @staticmethod
    def serialize_json(data):
        return json.dumps(data)
    
    
class SerializeAlbum(Serialize):
    def schema(self):
        return models.AlbumMeta(self.data)
    
    def serialize(self):
        return self.schema().__dict__
    
    def deserialize(self):
        return models.Album(**self.serialize(), album_data=self.data)
    
    