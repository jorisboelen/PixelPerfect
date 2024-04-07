from datetime import datetime
from pydantic import BaseModel
from typing import Union


class PhotoBase(BaseModel):
    album_id: int
    name: str
    date_taken: datetime
    file_name: str
    format: str
    mode: str
    width: int
    height: int
    exif_data: str


class Photo(PhotoBase):
    id: int
    date_created: datetime

    class Config:
        from_attributes = True


class AlbumBase(BaseModel):
    name: str


class Album(AlbumBase):
    id: int
    date_created: datetime
    cover_photo: Union[Photo, None] = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserLogin(UserBase):
    password: str

    class Config:
        from_attributes = True


class User(UserBase):
    is_admin: bool

    class Config:
        from_attributes = True


class Session(BaseModel):
    token: str
    username: str
    expires: datetime
