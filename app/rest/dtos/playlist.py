from typing import List
from pydantic.main import BaseModel
from app.rest.dtos.song import SongResponseDto


class PlaylistResponseDto(BaseModel):
    id: str
    title: str
    description: str
    songs: List[str] = []
    is_collaborative: bool
    owner_id: str

    def __getitem__(self, item):
        return getattr(self, item)


class PlaylistSongResponseDto(BaseModel):
    id: str
    title: str
    description: str
    songs: List[SongResponseDto] = []
    is_collaborative: bool
    owner_id: str

    def __getitem__(self, item):
        return getattr(self, item)

    def set_songs(self, songs=[]):
        self.songs = songs
