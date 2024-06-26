from sqlmodel import Session, select

from pixelperfect.db.models import Album, AlbumCreate, Photo, User


def get_album(db: Session, album_id: int):
    statement = select(Album).where(Album.id == album_id)
    return db.exec(statement).first()


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
    statement = select(Photo).where(Photo.id == photo_id)
    return db.exec(statement).first()


def create_photo(db: Session, photo: Photo):
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


def remove_photo(db: Session, photo: Photo):
    db.delete(photo)
    db.commit()


def get_user(db: Session, username: str):
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()


def update_user_password(db: Session, db_user: User, hashed_password: str):
    db_user.password = hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user
