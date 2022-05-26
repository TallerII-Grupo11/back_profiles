from pydantic.main import BaseModel


class UserResponseDto(BaseModel):
    firebase_id: str
    id: str
    first_name: str
    last_name: str
    role: str
    location: str
    email: str
