from typing import List
from pydantic.main import BaseModel
from app.rest.dtos.song import SongResponseDto



class PlaylistRequestDto(BaseModel):
    title: str
    description: str
    songs: List[str]
    is_collaborative: str
    owner_id: str


class PlaylistResponseDto(BaseModel):
    _id: str
    title: str
    description: str
    songs: List[str]
    is_collaborative: str
    owner_id: str

class PlaylistSongResponseDto(BaseModel):
    _id: str
    title: str
    description: str
    songs: List[SongResponseDto]
    is_collaborative: str
    owner_id: str
