from app.db.model.py_object_id import PyObjectId
from pydantic import Field

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId
from app.db.model.song import SongModel
from app.db.model.subscription import Subscription
from app.db.model.genre import Genre


class ProfileModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(...)
    interests: List[Genre] = []
    subscription: Subscription = Subscription.free
    own_playlists: List[str] = []
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
                "interests": ["genre1", "genre2"],
                "subscription": "free",
                "playlists": ["id1", "id2"],
                "follow_artists": ["id1"],
                "favorite_songs": ["song1", "song2"],
                "favorite_albums": [],
                "favorite_playlists": ["id1"]
            }
        }


class UpdateProfileModel(BaseModel):
    interests: Optional[List[str]]
    subscription: Optional[str]
    playlists: Optional[List[str]]
    follow_artists: Optional[List[str]]
    favorite_songs: Optional[List[str]]
    favorite_albums: Optional[List[str]]
    favorite_playlists: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "interests": ["genre1", "genre2"],
                "subscription": "free",
                "playlists": ["id1", "id2"],
                "follow_artists": ["id1"],
                "favorite_songs": ["song1", "song2"],
                "favorite_albums": [],
                "favorite_playlists": ["id1"]
            }
        }
