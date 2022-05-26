from pydantic.main import BaseModel


class UserRequestDto(BaseModel):
    firebase_id: str
    first_name: str
    last_name: str
    role: str
    location: str
    email: str
