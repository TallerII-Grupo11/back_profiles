import unittest
import httpx
import respx

from app.rest import MultimediaClient
from app.rest.dtos.album import AlbumResponseDto
from app.rest.dtos.artist import ArtistModel
from app.rest.dtos.playlist import PlaylistResponseDto
from app.rest.dtos.request.album import AlbumRequestDto
from app.rest.dtos.request.playlist import PlaylistRequestDto
from app.rest.dtos.request.song import SongRequestDto
from app.rest.dtos.song import SongResponseDto


def get_mocked_album_response(status_code: int, mock: AlbumResponseDto) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=mock.dict(),
    )


def get_album_response_mock() -> AlbumResponseDto:
    return AlbumResponseDto(
        id="id",
        title="title",
        artist=ArtistModel(artist_id="id", artist_name="name"),
        description="description",
        genre="genre",
        subscription="free",
        image="image",
    )


def get_mocked_song_response(status_code: int, mock: SongResponseDto) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=mock.dict(),
    )


def get_song_response_mock() -> SongResponseDto:
    return SongResponseDto(
        id="id",
        title="title",
        artists=[ArtistModel(artist_id="id", artist_name="name")],
        description="description",
        genre="genre",
        song_file="file",
    )


def get_mocked_playlist_response(status_code: int, mock: PlaylistResponseDto) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=mock.dict(),
    )


def get_playlist_response_mock() -> PlaylistResponseDto:
    return PlaylistResponseDto(
        id="id",
        title="title",
        songs=["song_id"],
        description="description",
        owner_id="user-id",
        is_collaborative=True,
    )


class TestMultimediaClient(unittest.TestCase):
    test_url = "https://test-api.com"

    @respx.mock
    def test_create_album(self, respx_mock):
        mock = get_album_response_mock()
        req = AlbumRequestDto(**mock.dict())
        respx_mock.post(f"{self.test_url}/albums", json=req.dict()).mock(
            return_value=get_mocked_album_response(201, mock))
        client = MultimediaClient(self.test_url)
        dto, album_id = client.create_album(req)

        assert dto.title == "title"
        assert album_id == "id"

    @respx.mock
    def test_create_album_error(self, respx_mock):
        mock = get_album_response_mock()
        req = AlbumRequestDto(**mock.dict())
        respx_mock.post(f"{self.test_url}/albums", json=req.dict()).mock(
            return_value=get_mocked_album_response(500, mock))
        client = MultimediaClient(self.test_url)
        self.assertRaises(
            Exception, client.create_album, req
        )

    @respx.mock
    def test_create_song(self, respx_mock):
        mock = get_song_response_mock()
        req = SongRequestDto(**mock.dict())
        respx_mock.post(f"{self.test_url}/songs", json=req.dict()).mock(
            return_value=get_mocked_song_response(201, mock))
        client = MultimediaClient(self.test_url)
        dto, album_id = client.create_song(req)

        assert dto.title == "title"
        assert album_id == "id"

    @respx.mock
    def test_create_song_error(self, respx_mock):
        mock = get_song_response_mock()
        req = SongRequestDto(**mock.dict())
        respx_mock.post(f"{self.test_url}/songs", json=req.dict()).mock(
            return_value=get_mocked_song_response(500, mock))
        client = MultimediaClient(self.test_url)
        self.assertRaises(
            Exception, client.create_song, req
        )

    @respx.mock
    def test_create_playlist(self, respx_mock):
        mock = get_playlist_response_mock()
        req = PlaylistRequestDto(**mock.dict())
        respx_mock.post(f"{self.test_url}/playlists/", json=req.dict()).mock(
            return_value=get_mocked_playlist_response(201, mock))
        client = MultimediaClient(self.test_url)
        dto, album_id = client.create_playlist(req)

        assert dto.title == "title"
        assert album_id == "id"

    @respx.mock
    def test_create_playlist_error(self, respx_mock):
        mock = get_playlist_response_mock()
        req = PlaylistRequestDto(**mock.dict())
        respx_mock.post(f"{self.test_url}/playlists/", json=req.dict()).mock(
            return_value=get_mocked_playlist_response(500, mock))
        client = MultimediaClient(self.test_url)
        self.assertRaises(
            Exception, client.create_playlist, req
        )

    @respx.mock
    def test_get_song(self, respx_mock):
        mock = get_song_response_mock()
        respx_mock.get(f"{self.test_url}/songs/id").mock(
            return_value=get_mocked_song_response(200, mock))
        client = MultimediaClient(self.test_url)
        dto = client.get_song("id")

        assert dto.title == "title"

    @respx.mock
    def test_create_song_error(self, respx_mock):
        mock = get_song_response_mock()
        respx_mock.get(f"{self.test_url}/songs/id").mock(
            return_value=get_mocked_song_response(500, mock))
        client = MultimediaClient(self.test_url)
        self.assertRaises(
            Exception, client.get_song, "id"
        )

    @respx.mock
    def test_get_album(self, respx_mock):
        mock = get_album_response_mock()
        respx_mock.get(f"{self.test_url}/albums/id").mock(
            return_value=get_mocked_album_response(200, mock))
        client = MultimediaClient(self.test_url)
        dto = client.get_album("id")

        assert dto.title == "title"

    @respx.mock
    def test_get_album_error(self, respx_mock):
        mock = get_album_response_mock()
        respx_mock.get(f"{self.test_url}/albums/id").mock(
            return_value=get_mocked_album_response(500, mock))
        client = MultimediaClient(self.test_url)
        self.assertRaises(
            Exception, client.get_album, "id"
        )

    # @respx.mock
    # def test_get_playlist(self, respx_mock):
    #     mock = get_playlist_response_mock()
    #     respx_mock.get(f"{self.test_url}/playlists/id").mock(
    #         return_value=get_mocked_playlist_response(200, mock))
    #     client = MultimediaClient(self.test_url)
    #     dto = client.get_playlist("id")
    #
    #     assert dto.title == "title"
    #
    # @respx.mock
    # def test_get_playlist_error(self, respx_mock):
    #     mock = get_playlist_response_mock()
    #     respx_mock.get(f"{self.test_url}/playlists/id").mock(
    #         return_value=get_mocked_playlist_response(500, mock))
    #     client = MultimediaClient(self.test_url)
    #     self.assertRaises(
    #         Exception, client.get_playlist, "id"
    #     )

