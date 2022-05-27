import httpx

from app.rest.dtos.user import UserResponseDto, UserRequestDto


class UserClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def create_user(self, request: UserRequestDto) -> UserResponseDto:
        r = httpx.post(f'{self.api_url}/users', data=request.dict())

        return UserResponseDto(**r.json())

    # test
    def get(self) -> UserResponseDto:
        r = httpx.get(f'{self.api_url}/users/62cf7d15-a12f-4881-8c6d-1bd82b766088')
        print(r.json())

        return UserResponseDto(**r.json())
