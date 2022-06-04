import httpx

from app.rest.dtos.request.user import UserRequestDto, UpdateUserRequestDto
from app.rest.dtos.user import UserResponseDto


class UserClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def create_user(self, request: UserRequestDto) -> UserResponseDto:
        print(request.dict())
        r = httpx.post(f'{self.api_url}/users', json=request.dict())
        if r.status_code != httpx.codes.CREATED:
            r.raise_for_status()

        return UserResponseDto(**r.json())

    def get(self, user_id: str) -> UserResponseDto:
        r = httpx.get(f'{self.api_url}/users/{user_id}')
        if r.status_code != httpx.codes.OK:
            r.raise_for_status()

        return UserResponseDto(**r.json())

    def update(self, user_id: str, request: UpdateUserRequestDto) -> UserResponseDto:
        r = httpx.put(f'{self.api_url}/users/{user_id}', json=request.dict())
        if r.status_code != httpx.codes.ACCEPTED:
            r.raise_for_status()

        return UserResponseDto(**r.json())
