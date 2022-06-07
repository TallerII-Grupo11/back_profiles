from typing import List

from pydantic.main import BaseModel

from app.rest.dtos.artist import ArtistModel


class SongRequestDto(BaseModel):
    title: str
    artists: List[ArtistModel]
    description: str
    song_file: str

    def __getitem__(self, item):
        return getattr(self, item)
