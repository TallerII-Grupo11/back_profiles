from app.conf.config import Settings
from functools import lru_cache


@lru_cache()
def get_settings():
    return Settings()
