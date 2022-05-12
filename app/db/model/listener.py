from app.db.model.py_object_id import PyObjectId
from pydantic import Field

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId
from app.db.model.subscription import Subscription


class ListenerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    firebase_id: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    country: str = Field(...)
    interests: List[str] = []
    subscription: Subscription = Subscription.free
    playlists: List[str] = []
    follow_artists: List[str] = []
    favorite_songs: List[str] = []
    favorite_albums: List[str] = []
    favorite_playlists: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "firebase_id": "firebase_id",
                "first_name": "",
                "last_name": "",
                "email": "email@gmail.com",
                "country": "country",
                "interests": ["genre1"]
            }
        }


class UpdateListenerModel(BaseModel):
    email: Optional[str]
    interest: Optional[str]
    subscription: Optional[str]
    playlist: Optional[str]
    follow_artist: Optional[str]
    favorite_song: Optional[str]
    favorite_album: Optional[str]
    favorite_playlist: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "email@gmail.com",
                "interest": "genre_name",
                "subscription": "free/normal/premium",
                "my_playlist": "id",
                "follow_artist": "id",
                "favorite_song": "id",
                "favorite_album": "id",
                "favorite_playlist": "id",
            }
        }
