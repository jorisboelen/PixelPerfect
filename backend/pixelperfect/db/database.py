from os import path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Session

from pixelperfect.core.settings import settings

SQLALCHEMY_URL = f"sqlite:///{path.join(settings.BASE_DIRECTORY, settings.SQLALCHEMY_DATABASE_FILE)}"

engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False}, pool_size=100, max_overflow=30)

Base = declarative_base()


def get_db():
    with Session(engine) as session:
        yield session
