from typing import List

from pydantic.main import BaseModel


class PlaylistRequestDto(BaseModel):
    title: str
    description: str
    songs: List[str]
    is_collaborative: bool
    owner_id: str

    def __getitem__(self, item):
        return getattr(self, item)
