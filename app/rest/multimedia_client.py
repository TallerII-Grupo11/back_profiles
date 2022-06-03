import httpx
import json
import logging

from typing import List
from app.rest.dtos.album import AlbumResponseDto, AlbumRequestDto, AlbumSongResponseDto
from app.rest.dtos.playlist import PlaylistResponseDto
from app.rest.dtos.playlist import PlaylistRequestDto, PlaylistSongResponseDto
from app.rest.dtos.song import SongResponseDto, SongRequestDto


class MultimediaClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def create_album(self, request: AlbumRequestDto) -> (AlbumResponseDto, str):
        r = httpx.post(f'{self.api_url}/albums', data=json.dumps(request.dict()))
        d = r.json()
        logging.info(f"[album] {d}")
        return AlbumResponseDto(**d), d["_id"]

    def create_song(self, request: SongRequestDto) -> (SongResponseDto, str):
        r = httpx.post(f'{self.api_url}/songs', data=json.dumps(request.dict()))
        d = r.json()

        return SongResponseDto(**d), d["_id"]

    def create_playlist(
        self, request: PlaylistRequestDto
    ) -> (PlaylistResponseDto, str):
        r = httpx.post(f'{self.api_url}/playlists', data=json.dumps(request.dict()))
        d = r.json()
        return PlaylistResponseDto(**d), d["_id"]

    def get_song(self, song_id: str) -> SongResponseDto:
        r = httpx.get(f'{self.api_url}/songs/{song_id}')
        d = r.json()

        return SongResponseDto(**d)

    def get_album(self, album_id: str) -> AlbumSongResponseDto:
        r = httpx.get(f'{self.api_url}/albums/{album_id}')
        s = r.json()
        songs_list = self.get_songs(s["songs"])

        del s["songs"]
        album = AlbumSongResponseDto(**s)
        album.set_songs(songs_list)

        return album

    def get_playlist(self, playlist_id: str) -> PlaylistSongResponseDto:
        r = httpx.get(f'{self.api_url}/playlists/{playlist_id}')
        s = r.json()
        songs_list = self.get_songs(s["songs"])

        del s["songs"]
        playlist = PlaylistSongResponseDto(**s)
        playlist.set_songs(songs_list)

        return playlist

    def get_songs(self, songs: List[str]) -> List[SongResponseDto]:
        songs_list = []
        for song_id in songs:
            s = self.get_song(song_id)
            songs_list.append(s)
        return songs_list

    def get_playlists(self, playlist_ids: List[str]) -> List[PlaylistSongResponseDto]:
        list_playlists = []

        for playlist_id in playlist_ids:
            play = self.get_playlist(playlist_id)
            list_playlists.append(play)

        return list_playlists

    def get_albums(self, album_ids: List[str]) -> List[AlbumSongResponseDto]:
        list_albums = []

        for album_id in album_ids:
            alb = self.get_album(album_id)
            list_albums.append(alb)

        return list_albums
