from fastapi import Depends
from app.conf.config import Settings, get_settings
from app.rest.users import UserClient


def get_restclient(settings: Settings = Depends(get_settings)) -> UserClient:
    return UserClient(settings.users_api)
