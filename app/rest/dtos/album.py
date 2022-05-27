from pydantic.main import BaseModel
from typing import List
from app.rest.dtos.song import SongRequestDto, SongResponseDto


class AlbumRequestDto(BaseModel):
    title: str
    artist: str
    description: str
    genre: str
    images: List[str]
    subscription: str
    songs: List[SongRequestDto]


class AlbumIdsRequestDto(BaseModel):
    title: str
    artist: str
    description: str
    genre: str
    images: List[str]
    subscription: str
    songs: List[str] = []


class AlbumResponseDto(BaseModel):
    _id: str
    title: str
    artist: str
    description: str
    genre: str
    images: List[str]
    subscription: str
    songs: List[str]


class AlbumSongResponseDto(BaseModel):
    _id: str
    title: str
    artist: str
    description: str
    genre: str
    images: List[str]
    subscription: str
    songs: List[SongResponseDto] = []
