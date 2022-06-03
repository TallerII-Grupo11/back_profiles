from fastapi import Depends
from app.conf.config import Settings, get_settings
from app.rest.users_client import UserClient
from app.rest.multimedia_client import MultimediaClient
import dataclasses, json


def get_restclient(settings: Settings = Depends(get_settings)) -> UserClient:
    return UserClient(settings.users_api)


def get_restmultimedia(settings: Settings = Depends(get_settings)) -> MultimediaClient:
    return MultimediaClient(settings.multimedia_api)
