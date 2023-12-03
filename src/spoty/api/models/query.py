from dataclasses import dataclass


@dataclass(frozen=True)
class Query:
    query: str
    type: str
    limit: int = 50
    features: bool = False
    time_format: bool = False
    
    def __post_init__(self):
        if self.type not in ["track", "artist", "album", "playlist"]:
            raise ValueError("Invalid type of search")
        if self.limit < 1:
            raise ValueError("Limit must be greater than 0")
