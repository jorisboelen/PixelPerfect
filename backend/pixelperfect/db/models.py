from datetime import datetime
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class AlbumCreate(SQLModel):
    name: str


class AlbumBase(SQLModel):
    name: str = Field(index=True, nullable=False)
    id: int | None = Field(default=None, primary_key=True)
    date_created: datetime | None = Field(default=None, index=True, nullable=False,
                                          sa_column_kwargs={"server_default": func.now()})
    cover_photo_id: int | None = Field(default=None, foreign_key="photos.id", nullable=True)


class Album(AlbumBase, table=True):
    __tablename__ = "albums"
    cover_photo: Optional["Photo"] = Relationship(sa_relationship_kwargs=dict(foreign_keys="[Album.cover_photo_id]"))


class Photo(SQLModel, table=True):
    __tablename__ = "photos"
    id: int | None = Field(default=None, primary_key=True)
    album_id: int = Field(foreign_key="albums.id", nullable=False)
    album: Album = Relationship(sa_relationship_kwargs=dict(foreign_keys="[Photo.album_id]"))
    name: str = Field(index=True, nullable=False)
    date_created: datetime | None = Field(default=None, index=True, nullable=False, sa_column_kwargs={"server_default": func.now()})
    date_taken: datetime = Field(index=True, nullable=False)
    file_name: str
    format: str
    mode: str
    width: int
    height: int
    exif_data: str


class AlbumWithCoverPhoto(AlbumBase):
    cover_photo: Photo | None = None


class UserBase(SQLModel):
    username: str = Field(primary_key=True)
    is_admin: bool = Field(nullable=False)


class User(UserBase, table=True):
    __tablename__ = "users"
    password: str = Field(nullable=False)


class UserLogin(SQLModel):
    username: str
    password: str


class UserSession(SQLModel):
    token: str
    username: str
    expires: datetime
