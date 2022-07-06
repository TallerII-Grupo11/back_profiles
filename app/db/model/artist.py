from app.db.model.py_object_id import PyObjectId
from pydantic import Field
from app.rest.dtos.album import AlbumSongResponseDto
from app.rest.dtos.song import SongResponseDto

from pydantic.main import BaseModel
from typing import List, Optional
from bson import ObjectId


class ArtistModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(...)
    albums: List[str] = []
    songs: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {"example": {"user_id": "user_id", "albums": [], "songs": []}}


class UpdateArtistModel(BaseModel):
    user_id: Optional[str]
    albums: Optional[List[str]]
    songs: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "user_id",
                "albums": [],
                "songs": [],
            }
        }


class CompleteArtistModel(BaseModel):
    user_id: Optional[str]
    albums: Optional[List[AlbumSongResponseDto]]
    songs: Optional[List[SongResponseDto]]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "user_id",
                "albums": [],
                "songs": [],
            }
        }
