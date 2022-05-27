from pydantic.main import BaseModel

class AlbumRequestDto(BaseModel):
    title: str
    artist: str
    description: str
    genre: str
    images: List[str]
    subscription: str
    songs: List[str]

class AlbumResponseDto(BaseModel):
    _id: str
    title: str
    artist: str
    description: str
    genre: str
    images: List[str]
    subscription: str
    songs: List[str]
