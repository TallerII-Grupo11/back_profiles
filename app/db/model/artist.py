from app.db.model.py_object_id import PyObjectId
from pydantic import Field

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId


class ArtistModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    country: str = Field(...)
    firebase_id: str = Field(...)
    songs: List[str] = []
    albums: List[str] = []

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
                "country": "country"
            }
        }


class UpdateArtistModel(BaseModel):
    song: Optional[str]
    album: Optional[str]
    email: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "song": "id",
                "album": "id",
                "email": "email@gmail.com"
            }
        }
