import httpx

from app.rest.dtos.album import AlbumResponseDto, AlbumRequestDto
from app.rest.dtos.playlist import PlaylistResponseDto, PlaylistRequestDto
from app.rest.dtos.song import SongResponseDto, SongRequestDto


class MultimediaClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def create_album(self, request: AlbumRequestDto) -> AlbumResponseDto:
        song_ids = []
        for song in request["songs"]:
            s = self.create_song(song)
            song_ids.append(s["_id"])
        del request["songs"]

        album = AlbumIdsRequestDto(**request.json())
        album["songs"] = song_ids
        r = httpx.post(f'{self.api_url}/albums', data=album.dict())

        return AlbumResponseDto(**r.json())

    def create_song(self, request: SongRequestDto) -> SongResponseDto:
        r = httpx.post(f'{self.api_url}/songs', data=request.dict())

        return SongResponseDto(**r.json())

    def create_playlist(self, request: PlaylistRequestDto) -> PlaylistResponseDto:
        r = httpx.post(f'{self.api_url}/playlists', data=request.dict())

        return PlaylistResponseDto(**r.json())

    def get_song(self, song_id: str) -> SongResponseDto:
        r = httpx.get(f'{self.api_url}/songs/{song_id}')
        print(r.json())

        return SongResponseDto(**r.json())

    def get_album(self, album_id: str) -> AlbumSongResponseDto:
        r = httpx.get(f'{self.api_url}/album/{song_id}')
        songs_list = []
        for song_id in r["songs"]:
            s = self.get_song(song_id)
            songs_list.append(s)

        del r["songs"]
        album = AlbumSongResponseDto(**r.json())
        album["songs"] = songs_list

        return album

    def get_playlist(self, playlist_id: str) -> PlaylistSongResponseDto:
        r = httpx.get(f'{self.api_url}/playlists/{playlist_id}')
        songs_list = []
        for song_id in r["songs"]:
            s = self.get_song(song_id)
            songs_list.append(s)

        del r["songs"]
        playlist = PlaylistSongResponseDto(**r.json())
        playlist["songs"] = songs_list

        return playlist
