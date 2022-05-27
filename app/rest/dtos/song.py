from pydantic.main import BaseModel


class SongRequestDto(BaseModel):
    title: str
    artists: List[str]
    description: str
    song_file: str

class SongResponseDto(BaseModel):
    _id: str
    title: str
    artists: List[str]
    description: str
    song_file: str