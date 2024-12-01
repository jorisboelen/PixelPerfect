from pixelperfect.core.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Session

database_url = str(settings.sqlalchemy_database_url)
database_connect_args = {"check_same_thread": False} if settings.DATABASE_SCHEME == 'sqlite' else {}

engine = create_engine(url=database_url, connect_args=database_connect_args, pool_size=200, max_overflow=50)

Base = declarative_base()


def get_db():
    with Session(engine) as session:
        yield session
