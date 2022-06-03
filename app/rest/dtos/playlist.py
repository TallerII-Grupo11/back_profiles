from typing import List
from pydantic.main import BaseModel
from app.rest.dtos.song import SongResponseDto


class PlaylistRequestDto(BaseModel):
    title: str
    description: str
    songs: List[str]
    is_collaborative: str
    owner_id: str

    def __getitem__(self, item):
        return getattr(self, item)


class PlaylistResponseDto(BaseModel):
    _id: str
    title: str
    description: str
    songs: List[str] = []
    is_collaborative: str
    owner_id: str

    def __getitem__(self, item):
        return getattr(self, item)


class PlaylistSongResponseDto(BaseModel):
    _id: str
    title: str
    description: str
    songs: List[SongResponseDto] = []
    is_collaborative: str
    owner_id: str

    def __getitem__(self, item):
        return getattr(self, item)

    def set_songs(self, songs=[]):
        self.songs = songs
