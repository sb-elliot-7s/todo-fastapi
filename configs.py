from functools import lru_cache
from pydantic import BaseSettings
from pathlib import Path

IMAGES_DIR = str(Path(__file__).resolve().parent.joinpath('images'))


class Configs(BaseSettings):
    database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    image_host: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Configs:
    return Configs()
