from os import makedirs, path
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    BASE_DIRECTORY: str = path.join(Path.home(), '.pixelperfect')
    CORS_ALLOWED_ORIGINS: List[str] = []
    IMAGE_RESIZE_SIZES: List[int] = [1920]
    SESSION_EXPIRE_SECONDS: int = 86400
    SQLALCHEMY_DATABASE_FILE: str = "pixelperfect.db"


settings = Settings(_env_file=('development.env', 'settings.env'), _env_file_encoding='utf-8')

makedirs(settings.BASE_DIRECTORY, exist_ok=True)
