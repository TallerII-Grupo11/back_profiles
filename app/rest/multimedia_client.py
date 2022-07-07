import httpx
import json
import logging

from typing import List
from app.rest.dtos.album import AlbumResponseDto, AlbumSongResponseDto
from app.rest.dtos.request.album import AlbumRequestDto
from app.rest.dtos.playlist import PlaylistResponseDto, PlaylistSongResponseDto
from app.rest.dtos.request.playlist import PlaylistRequestDto
from app.rest.dtos.song import SongResponseDto
from app.rest.dtos.request.song import SongRequestDto


class MultimediaClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def create_album(self, request: AlbumRequestDto) -> (AlbumResponseDto, str):
        r = httpx.post(f'{self.api_url}/albums', json=request.dict())

        if r.status_code != httpx.codes.CREATED:
            r.raise_for_status()

        d = r.json()
        logging.info(f"[album] {d}")
        return AlbumResponseDto(**d), d["id"]

    def create_song(self, request: SongRequestDto) -> (SongResponseDto, str):
        r = httpx.post(f'{self.api_url}/songs', json=request.dict())
        if r.status_code != httpx.codes.CREATED:
            r.raise_for_status()

        d = r.json()

        return SongResponseDto(**d), d["id"]

    def create_playlist(
        self, request: PlaylistRequestDto
    ) -> (PlaylistResponseDto, str):
        r = httpx.post(f'{self.api_url}/playlists/', json=request.dict())

        if r.status_code != httpx.codes.CREATED:
            r.raise_for_status()

        d = r.json()
        logging.info(f"[PLAYLIST JSON] {d}")
        return PlaylistResponseDto(**d), d["id"]

    def get_song(self, song_id: str) -> SongResponseDto:
        r = httpx.get(f'{self.api_url}/songs/{song_id}')
        if r.status_code != httpx.codes.OK:
            r.raise_for_status()

        d = r.json()

        return SongResponseDto(**d)

    def get_album(self, album_id: str) -> AlbumSongResponseDto:
        r = httpx.get(f'{self.api_url}/albums/{album_id}')
        if r.status_code != httpx.codes.OK:
            r.raise_for_status()

        s = r.json()
        logging.info(s)
        # songs_list = self.get_songs(s["songs"])

        # del s["songs"]
        album = AlbumSongResponseDto(**s)
        # album.set_songs(songs_list)

        return album

    def get_playlist(self, playlist_id: str) -> PlaylistSongResponseDto:
        r = httpx.get(f'{self.api_url}/playlists/{playlist_id}')
        if r.status_code != httpx.codes.OK:
            r.raise_for_status()

        s = r.json()
        songs_list = self.get_songs(s["songs"])

        del s["songs"]
        playlist = PlaylistSongResponseDto(**s)
        playlist.set_songs(songs_list)

        return playlist

    def get_songs(self, songs: List[str]) -> List[SongResponseDto]:
        songs_list = []
        for song_id in songs:
            try:
                s = self.get_song(song_id)
                songs_list.append(s)
            except Exception as e:
                logging.error(f"Error getting song {song_id}. Exception {e}")

        return songs_list

    def get_playlists(self, playlist_ids: List[str]) -> List[PlaylistSongResponseDto]:
        list_playlists = []

        for playlist_id in playlist_ids:
            try:
                play = self.get_playlist(playlist_id)
                list_playlists.append(play)
            except Exception as e:
                logging.error(f"Error getting playlist {playlist_id}. Exception {e}")

        return list_playlists

    def get_albums(self, album_ids: List[str]) -> List[AlbumSongResponseDto]:
        list_albums = []

        for album_id in album_ids:
            alb = self.get_album(album_id)
            list_albums.append(alb)

        return list_albums

    def add_song_to_album(self, album_id: str, song_id=str) -> bool:
        song = {"songs": [song_id]}
        r = httpx.patch(
            f'{self.api_url}/albums/{album_id}/songs', data=json.dumps(song)
        )
        return r.status_code == 200

    def get_songs_by_genre(self, genre: str) -> List[SongResponseDto]:
        r = httpx.get(f'{self.api_url}/songs?genre={genre}')
        if r.status_code != httpx.codes.OK:
            r.raise_for_status()

        logging.debug(f"RECOMMENDATION: --> {r}")
        response = r.json()

        songs_list = []
        for s in response:
            songs_list.append(SongResponseDto(**s))
        return songs_list

    def get_recomendation_by_genre(self, interests: List[str]) -> List[SongResponseDto]:
        songs_list = []
        for genre in interests[:2]:
            songs = self.get_songs_by_genre(genre)
            for song in songs[:3]:
                songs_list.append(song)
        return songs_list[:10]
