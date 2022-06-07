from app.db.model.py_object_id import PyObjectId
from pydantic import Field
from app.rest.dtos.playlist import PlaylistSongResponseDto

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId


class ListenerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(...)
    interests: List[str] = []
    playlists: List[str] = []
    subscription: str = "free"
    #    playlists: List[str] = []
    #    follow_artists: List[str] = []
    #    favorite_songs: List[str] = []
    #    favorite_albums: List[str] = []
    #    favorite_playlists: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "id",
                "interests": ["genre_name"],
                "playlists": ["playlist_ids"],
                "subscription": "free"
            }
        }


class UpdateListenerModel(BaseModel):
    interests: Optional[List[str]]
    playlists: Optional[List[str]]
    subscription: Optional[str]
    #    follow_artist: Optional[str]
    #    favorite_song: Optional[str]
    #    favorite_album: Optional[str]
    #    favorite_playlist: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "id",
                "interests": ["genre_name"],
                "playlists": ["playlist_ids"],
                "subscription": "free"
            }
        }


class CompleteListenerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(...)
    interests: List[str] = []
    playlists: List[PlaylistSongResponseDto] = []
    subscription: str = "free"

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
