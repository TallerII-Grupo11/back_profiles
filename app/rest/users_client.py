from typing import List

import httpx
from pydantic.tools import parse_obj_as

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

    def all(self, user_ids: str = None) -> List[UserResponseDto]:
        qp = f"?user_ids={user_ids}" if user_ids else ""
        r = httpx.get(f'{self.api_url}/users{qp}')
        if r.status_code != httpx.codes.OK:
            r.raise_for_status()

        return parse_obj_as(List[UserResponseDto], r.json())

    def update(self, user_id: str, request: UpdateUserRequestDto) -> UserResponseDto:
        r = httpx.put(f'{self.api_url}/users/{user_id}', json=request.dict())
        if r.status_code != httpx.codes.ACCEPTED:
            r.raise_for_status()

        return UserResponseDto(**r.json())
