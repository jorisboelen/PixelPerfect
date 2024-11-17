from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Session

from pixelperfect.core.settings import settings

engine = create_engine(url=str(settings.sqlalchemy_database_url),
                       connect_args={"check_same_thread": False},
                       pool_size=100, max_overflow=30)

Base = declarative_base()


def get_db():
    with Session(engine) as session:
        yield session
