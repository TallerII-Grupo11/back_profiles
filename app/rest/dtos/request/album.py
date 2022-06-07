from typing import List

from pydantic.main import BaseModel

from app.rest.dtos.artist import ArtistModel


class AlbumRequestDto(BaseModel):
    title: str
    artist: ArtistModel
    description: str
    genre: str
    image: str
    subscription: str
    songs: List[str] = []

    def __getitem__(self, item):
        return getattr(self, item)

    def set_songs(self, songs=[]):
        self.songs = songs
