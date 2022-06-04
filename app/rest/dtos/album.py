from pydantic.main import BaseModel
from typing import List
from app.rest.dtos.song import SongResponseDto
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


class AlbumResponseDto(BaseModel):
    _id: str
    title: str
    artist: ArtistModel
    description: str
    genre: str
    image: str
    subscription: str
    songs: List[str] = []

    def __getitem__(self, item):
        return getattr(self, item)


class AlbumSongResponseDto(BaseModel):
    _id: str
    title: str
    artist: ArtistModel
    description: str
    genre: str
    image: str
    subscription: str
    songs: List[SongResponseDto] = []

    def __getitem__(self, item):
        return getattr(self, item)

    def set_songs(self, songs=[]):
        self.songs = songs
