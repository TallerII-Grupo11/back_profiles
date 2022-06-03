from pydantic.main import BaseModel
from typing import List


class SongRequestDto(BaseModel):
    title: str
    artists: List[str]
    description: str
    song_file: str

    def __getitem__(self, item):
        return getattr(self, item)


class SongResponseDto(BaseModel):
    _id: str
    title: str
    artists: List[str]
    description: str
    song_file: str

    def __getitem__(self, item):
        return getattr(self, item)

    def __dict__(self):
        return {"id": self._id,
                "title": self.title,
                "artists": self.artists,
                "description": self.description,
                "song_file": self.song_file
        }
