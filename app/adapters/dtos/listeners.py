from typing import List, Optional

from pydantic.fields import Field
from pydantic.main import BaseModel

from app.db.model.listener import ListenerModel, CompleteListenerModel
from app.rest.dtos.playlist import PlaylistSongResponseDto
from app.rest.dtos.user import UserResponseDto


class ListenerRequestDto(BaseModel):
    firebase_id: str = Field(example="123e4567-e89b-12d3-a456-426614174000")
    email: str = Field(example="user@mail.com")
    first_name: str = Field(example="Juan")
    last_name: str = Field(example="Perez")
    location: Optional[str] = Field(example="Argentina")
    interests: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        # schema_extra = {"example": {"user_id": "user_id", "songs": [], "albums": []}}


class UpdateListenerRequestDto(ListenerRequestDto):
    status: Optional[str] = Field(example="ACTIVE")


class ListenerResponseDto(BaseModel):
    id: str = Field(example="123asd-456fgh")
    user_id: str = Field(...)
    firebase_id: str = Field(example="123e4567-e89b-12d3-a456-426614174000")
    email: str = Field(example="user@mail.com")
    first_name: str = Field(example="Juan")
    last_name: str = Field(example="Perez")
    location: Optional[str] = Field(example="Argentina")
    status: Optional[str] = Field(example="ACTIVE")
    role: str = Field(example="LISTENER")
    subscription: str = Field(default="free", example="free")
    interests: List[str] = []
    playlists: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        # schema_extra = {"example": {"user_id": "user_id", "songs": [], "albums": []}}

    @staticmethod
    def from_listener_model(listener_model: ListenerModel, user: UserResponseDto) -> "ListenerResponseDto":
        return ListenerResponseDto(
            id=str(listener_model.id),
            user_id=user.id,
            firebase_id=user.firebase_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            location=user.location,
            status=user.status,
            role=user.role,
            interests=listener_model.interests,
            subscription=listener_model.subscription,
            playlists=listener_model.playlists,
        )


class CompleteListenerResponseDto(ListenerResponseDto):
    playlists: List[PlaylistSongResponseDto] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        # schema_extra = {"example": {"user_id": "user_id", "songs": [], "albums": []}}

    @staticmethod
    def from_models(
            listener_model: ListenerModel,
            user: UserResponseDto,
            complete_listener_model: CompleteListenerModel,
    ) -> "CompleteListenerResponseDto":
        return CompleteListenerResponseDto(
            id=str(listener_model.id),
            user_id=user.id,
            firebase_id=user.firebase_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            location=user.location,
            status=user.status,
            role=user.role,
            interests=listener_model.interests,
            subscription=listener_model.subscription,
            playlists=complete_listener_model.playlists,
        )

