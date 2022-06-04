from typing import Optional

from pydantic.main import BaseModel


class UserResponseDto(BaseModel):
    firebase_id: str
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    location: Optional[str]
    status: str
