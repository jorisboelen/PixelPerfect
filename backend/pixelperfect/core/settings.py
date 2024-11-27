from os import makedirs, path
from pathlib import Path
from pydantic import computed_field, Field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from typing import List, Literal


class Settings(BaseSettings):
    BASE_DIRECTORY: str = path.join(Path.home(), '.pixelperfect')
    IMAGE_DIRECTORY: str = path.join(BASE_DIRECTORY, "images")
    CORS_ALLOWED_ORIGINS: List[str] = Field(default_factory=list)
    IMAGE_RESIZE_SIZES: List[int] = Field(default=[1920])
    SESSION_EXPIRE_SECONDS: int = 86400

    # database settings
    DATABASE_SCHEME: Literal['postgresql', 'mysql', 'sqlite'] = 'sqlite'
    DATABASE_FILE: str = 'pixelperfect.db'
    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: int | None = None
    DATABASE_DB: str = 'pixelperfect'
    DATABASE_USER: str = 'pixelperfect'
    DATABASE_PASSWORD: str | None = None
    DATABASE_PARAMETERS: str | None = None

    @computed_field
    @property
    def sqlalchemy_database_url(self) -> MultiHostUrl:
        if self.DATABASE_SCHEME == 'sqlite':
            return MultiHostUrl.build(
                scheme=self.DATABASE_SCHEME,
                host="",
                path=path.join(self.BASE_DIRECTORY, self.DATABASE_FILE),
                query=self.DATABASE_PARAMETERS
            )
        else:
            return MultiHostUrl.build(
                scheme=self.DATABASE_SCHEME + ('+pymysql' if self.DATABASE_SCHEME == 'mysql' else ''),
                username=self.DATABASE_USER,
                password=self.DATABASE_PASSWORD,
                host=self.DATABASE_HOST,
                port=self.DATABASE_PORT,
                path=self.DATABASE_DB,
                query=self.DATABASE_PARAMETERS
            )


settings = Settings(_env_file=('development.env', 'settings.env'), _env_file_encoding='utf-8')

makedirs(settings.BASE_DIRECTORY, exist_ok=True)
