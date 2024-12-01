from cachetools import cached, TTLCache
from sqlmodel import Session, select
from pixelperfect.db.database import get_db
from pixelperfect.db.models import Album, AlbumCreate, Photo, User, UserSession


def get_album(db: Session, album_id: int):
    return db.get(Album, album_id)


def get_album_photos(db: Session, album_id: int):
    statement = select(Photo).where(Photo.album_id == album_id).order_by(Photo.date_taken, Photo.name)
    return db.exec(statement)


def get_albums(db: Session):
    statement = select(Album).order_by(Album.name)
    return db.exec(statement).all()


def create_album(db: Session, album: Album):
    db.add(album)
    db.commit()
    db.refresh(album)
    return album


def update_album(db: Session, db_album: Album, album: AlbumCreate):
    db_album.name = album.name
    db.commit()
    db.refresh(db_album)
    return db_album


def update_album_cover(db: Session, db_album: Album, cover_photo_id: int):
    db_album.cover_photo_id = cover_photo_id
    db.commit()
    db.refresh(db_album)
    return db_album


def remove_album(db: Session, album: Album):
    db.delete(album)
    db.commit()


def get_photo(db: Session, photo_id: int):
    return db.get(Photo, photo_id)


def create_photo(db: Session, photo: Photo):
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


def remove_photo(db: Session, photo: Photo):
    db.delete(photo)
    db.commit()


def get_user(db: Session, username: str):
    return db.get(User, username)


def update_user_password(db: Session, db_user: User, hashed_password: str):
    db_user.password = hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_session(db: Session, session_token: str):
    return db.get(UserSession, session_token)


@cached(TTLCache(maxsize=1024, ttl=30))
def get_user_session_cached(session_token: str):
    return get_user_session(db=next(get_db()), session_token=session_token)


def create_user_session(db: Session, user_session: UserSession):
    db.add(user_session)
    db.commit()
    db.refresh(user_session)
    return user_session


def remove_user_session(db: Session, session_token: str):
    user_session = db.get(UserSession, session_token)
    if user_session:
        db.delete(user_session)
        db.commit()
