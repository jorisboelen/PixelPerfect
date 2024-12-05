import pytest
import pixelperfect
from alembic.command import upgrade
from alembic.config import Config
from datetime import datetime, timedelta
from faker import Faker
from faker.providers import address
from os import path
from pixelperfect.core.settings import settings
from pixelperfect.db import crud
from pixelperfect.db.database import get_db
from pixelperfect.db.models import Album, AlbumCreate, UserSession
from secrets import token_hex

fake = Faker()
fake.add_provider(address)

def generate_user_token(username: str, save_to_db: bool=True):
    token = UserSession(token=token_hex(), username=username,
                        expires=datetime.now() + timedelta(seconds=settings.SESSION_EXPIRE_SECONDS))
    if save_to_db:
        crud.create_user_session(db=next(get_db()), user_session=token)
    return token


@pytest.fixture(autouse=True)
def alembic_upgrade():
    config = Config(file_=path.join(path.dirname(pixelperfect.__file__), "alembic.ini"))
    config.set_main_option("script_location", path.join(path.dirname(pixelperfect.__file__), "alembic"))
    upgrade(config, "head")


@pytest.fixture()
def album():
    return crud.create_album(db=next(get_db()), album=Album(name=fake.country()))


@pytest.fixture()
def album_create():
    return AlbumCreate(name=fake.city())


@pytest.fixture()
def users():
    return {
        'correct': [
            {'username': 'admin', 'password': 'pixelperfect'},
            {'username': 'viewer', 'password': 'pixelperfect'}
        ],
        'incorrect_password': [
            {'username': 'admin', 'password': 'incorrect123'},
            {'username': 'viewer', 'password': 'incorrect123'}
        ],
        'incorrect_username': [
            {'username': 'incorrectadmin', 'password': 'incorrect123', 'is_admin': True},
            {'username': 'incorrectviewer', 'password': 'pixelperfect', 'is_admin': False}
        ]
    }


@pytest.fixture()
def user_tokens():
    return {
        'correct': [generate_user_token('admin'), generate_user_token('viewer')],
        'incorrect': [generate_user_token('admin', False), generate_user_token('viewer', False)]
    }
