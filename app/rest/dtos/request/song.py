from pydantic.main import BaseModel


class SongRequestDto(BaseModel):
    title: str
    artists: List[str]
    description: str
    song_file: str