from typing import List, Optional

from pydantic.fields import Field
from pydantic.main import BaseModel

from app.db.model.artist import ArtistModel, CompleteArtistModel
from app.rest.dtos.album import AlbumSongResponseDto
from app.rest.dtos.song import SongResponseDto
from app.rest.dtos.user import UserResponseDto


class ArtistRequestDto(BaseModel):
    firebase_id: str = Field(example="123e4567-e89b-12d3-a456-426614174000")
    email: str = Field(example="user@mail.com")
    first_name: str = Field(example="Juan")
    last_name: str = Field(example="Perez")
    location: Optional[str] = Field(example="Argentina")
    songs: List[str] = []
    albums: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        # schema_extra = {"example": {"user_id": "user_id", "songs": [], "albums": []}}


class UpdateArtistRequestDto(ArtistRequestDto):
    status: Optional[str] = Field(example="ACTIVE")


class ArtistResponseDto(BaseModel):
    id: str = Field(example="123asd-456fgh")
    user_id: str = Field(...)
    firebase_id: str = Field(example="123e4567-e89b-12d3-a456-426614174000")
    email: str = Field(example="user@mail.com")
    first_name: str = Field(example="Juan")
    last_name: str = Field(example="Perez")
    location: Optional[str] = Field(example="Argentina")
    status: Optional[str] = Field(example="ACTIVE")
    role: str = Field(example="ARTIST")
    songs: List[str] = []
    albums: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        # schema_extra = {"example": {"user_id": "user_id", "songs": [], "albums": []}}

    @staticmethod
    def from_artist_model(
        artist_model: ArtistModel,
        user: UserResponseDto,
    ) -> "ArtistResponseDto":
        return ArtistResponseDto(
            id=str(artist_model.id),
            user_id=user.id,
            firebase_id=user.firebase_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            location=user.location,
            status=user.status,
            role=user.role,
            songs=artist_model.songs,
            albums=artist_model.albums,
        )


class CompleteArtistResponseDto(ArtistResponseDto):
    albums: List[AlbumSongResponseDto] = []
    songs: List[SongResponseDto] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        # schema_extra = {"example": {"user_id": "user_id", "songs": [], "albums": []}}

    @staticmethod
    def from_models(
        artist_model: ArtistModel,
        user: UserResponseDto,
        complete_artist_model: CompleteArtistModel,
        artist_id=None
    ) -> "CompleteArtistResponseDto":
        if artist_id is None:
            artist_id = artist_model.id
        return CompleteArtistResponseDto(
            id=str(artist_id),
            user_id=user.id,
            firebase_id=user.firebase_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            location=user.location,
            status=user.status,
            role=user.role,
            songs=complete_artist_model.songs,
            albums=complete_artist_model.albums,
        )
