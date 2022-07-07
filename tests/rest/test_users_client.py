import unittest
import httpx
import respx

from app.rest import UserClient
from app.rest.dtos.request.user import UserRequestDto, UpdateUserRequestDto
from app.rest.dtos.user import UserResponseDto


def get_mocked_response(status_code: int, mock: UserResponseDto) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=mock.dict(),
    )


def get_user_response_mock() -> UserResponseDto:
    return UserResponseDto(
        firebase_id="asd",
        id="id",
        email="mail@mail.com",
        first_name="name",
        last_name="lastname",
        role="LISTENER",
        location="Buenos Aires",
        status="ACTIVE",
    )


class TestUserClient(unittest.TestCase):
    test_url = "https://test-api.com"

    @respx.mock
    def test_create_user(self, respx_mock):
        mock = get_user_response_mock()
        req = UserRequestDto(**mock.dict())
        respx_mock.post(f"{self.test_url}/users", json=req.dict()).mock(
            return_value=get_mocked_response(201, mock))
        client = UserClient(self.test_url)
        dto = client.create_user(req)

        assert dto.id == "id"

    @respx.mock
    def test_create_user_error(self, respx_mock):
        mock = get_user_response_mock()
        req = UserRequestDto(**mock.dict())
        respx_mock.post(f"{self.test_url}/users", json=req.dict()).mock(
            return_value=get_mocked_response(500, mock))
        client = UserClient(self.test_url)
        self.assertRaises(
            Exception, client.create_user, req
        )

    @respx.mock
    def test_get_user(self, respx_mock):
        mock = get_user_response_mock()
        respx_mock.get(f"{self.test_url}/users/id").mock(
            return_value=get_mocked_response(200, mock))
        client = UserClient(self.test_url)
        dto = client.get("id")

        assert dto.id == "id"

    @respx.mock
    def test_all_with_query(self, respx_mock):
        mock = get_user_response_mock()
        respx_mock.get(f"{self.test_url}/users?user_ids=123").mock(
            return_value=httpx.Response(
                status_code=200,
                json=[mock.dict()],
            ))
        client = UserClient(self.test_url)
        dto = client.all("123")

        assert len(dto) == 1

    @respx.mock
    def test_all(self, respx_mock):
        mock = get_user_response_mock()
        mock2 = get_user_response_mock()
        respx_mock.get(f"{self.test_url}/users").mock(
            return_value=httpx.Response(
                status_code=200,
                json=[mock.dict(), mock2.dict()],
            ))
        client = UserClient(self.test_url)
        dto = client.all()

        assert len(dto) == 2

    @respx.mock
    def test_all_error(self, respx_mock):
        mock = get_user_response_mock()
        req = UserRequestDto(**mock.dict())
        respx_mock.get(f"{self.test_url}/users").mock(
            return_value=httpx.Response(
                status_code=500,
                json=mock.dict(),
            ))
        client = UserClient(self.test_url)
        self.assertRaises(
            Exception, client.all, None
        )

    @respx.mock
    def test_update(self, respx_mock):
        mock = get_user_response_mock()
        req = UpdateUserRequestDto(**mock.dict())
        respx_mock.put(f"{self.test_url}/users/123", json=req.dict()).mock(
            return_value=httpx.Response(
                status_code=202,
                json=mock.dict(),
            ))
        client = UserClient(self.test_url)
        dto = client.update("123", req)

        assert dto.id == "id"

    @respx.mock
    def test_update_error(self, respx_mock):
        mock = get_user_response_mock()
        req = UpdateUserRequestDto(**mock.dict())
        respx_mock.put(f"{self.test_url}/users/123", json=req.dict()).mock(
            return_value=httpx.Response(
                status_code=500,
                json=mock.dict(),
            ))
        client = UserClient(self.test_url)
        self.assertRaises(
            Exception, client.all, "123", req
        )
