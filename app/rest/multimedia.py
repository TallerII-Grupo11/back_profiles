import httpx

from app.rest.dtos.request.album import AlbumRequestDto
from app.rest.dtos.album import AlbumResponseDto


class MultimediaClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def create_album(self, request: AlbumRequestDto) -> AlbumResponseDto:
        r = httpx.post(f'{self.api_url}/albums', data=request.dict())

        return AlbumResponseDto(**r.json())

    def create_song(self, request: SongRequestDto) -> SongResponseDto:
        r = httpx.post(f'{self.api_url}/songs', data=request.dict())

        return SongResponseDto(**r.json())

    def create_playlist(self, request: PlaylistsRequestDto) -> PlaylistsResponseDto:
        r = httpx.post(f'{self.api_url}/playlists', data=request.dict())

        return PlaylistsResponseDto(**r.json())
