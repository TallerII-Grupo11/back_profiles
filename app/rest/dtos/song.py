from pydantic.main import BaseModel
from typing import List
from app.rest.dtos.artist import ArtistModel


class SongResponseDto(BaseModel):
    _id: str
    title: str
    artists: List[ArtistModel]
    description: str
    song_file: str

    def __getitem__(self, item):
        return getattr(self, item)
