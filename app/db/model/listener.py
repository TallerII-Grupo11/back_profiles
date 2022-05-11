from app.db.model.py_object_id import PyObjectId
from pydantic import Field

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId
from app.db.model.subscription import Subscription
from app.db.model.genre import Genre


class ListenerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(...)
    interests: List[Genre] = []
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
                "user_id": "user_id"
            }
        }
