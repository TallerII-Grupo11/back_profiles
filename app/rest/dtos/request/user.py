from typing import Optional

from pydantic.main import BaseModel


class UserRequestDto(BaseModel):
    firebase_id: str
    first_name: str
    last_name: str
    role: str
    location: Optional[str]
    email: str


class UpdateUserRequestDto(UserRequestDto):
    status: Optional[str]
