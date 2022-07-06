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
    wallet_addr: str = ""

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "id",
                "interests": ["genre_name"],
                "playlists": ["playlist_ids"],
                "subscription": "free",
                "wallet_addr": ""
            }
        }


class UpdateListenerModel(BaseModel):
    interests: Optional[List[str]]
    playlists: Optional[List[str]]
    subscription: Optional[str]
    wallet_addr: Optional[str]


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "id",
                "interests": ["genre_name"],
                "playlists": ["playlist_ids"],
                "subscription": "free",
                "wallet_addr": ""
            }
        }


class CompleteListenerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(...)
    interests: List[str] = []
    playlists: List[PlaylistSongResponseDto] = []
    subscription: str = "free"
    wallet_addr: str = ""

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
