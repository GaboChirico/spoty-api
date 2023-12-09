from dataclasses import dataclass


@dataclass(frozen=True)
class Query:
    query: str
    type: str
    limit: int = 50
    features: bool = False

    def __post_init__(self):
        if self.type not in ["track", "artist", "album", "playlist"]:
            raise ValueError("Invalid type of search")
        if self.limit < 1:
            raise ValueError("Limit must be greater than 0")

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"
