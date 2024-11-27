from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile
from sqlmodel import Session

from pixelperfect.api.endpoints.photos import delete_photo
from pixelperfect.db import crud
from pixelperfect.db.database import get_db
from pixelperfect.db.models import Album, AlbumCreate, AlbumWithCoverPhoto, Photo
from pixelperfect.utils import process_photo_upload, save_photo_upload

router = APIRouter()


@router.get("/", response_model=list[AlbumWithCoverPhoto], status_code=200)
def read_albums(db: Session = Depends(get_db)):
    albums = crud.get_albums(db)
    return albums


@router.post("/", response_model=Album, status_code=201)
def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
    return crud.create_album(db=db, album=Album.model_validate(album))


@router.get("/{album_id}", response_model=Album, status_code=200)
def read_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.get_album(db=db, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@router.put("/{album_id}", response_model=Album, status_code=200)
def update_album(album_id: int, album: AlbumCreate, db: Session = Depends(get_db)):
    db_album = crud.get_album(db=db, album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=404, detail="Album not found")
    return crud.update_album(db=db, db_album=db_album, album=album)


@router.delete("/{album_id}", status_code=204)
def delete_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.get_album(db=db, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    for photo in crud.get_album_photos(db=db, album_id=album_id):
        delete_photo(photo_id=photo.id, db=db)
    crud.remove_album(db=db, album=album)


@router.put("/{album_id}/cover", response_model=Album, status_code=200)
def set_album_cover(album_id: int, cover_photo_id: int, db: Session = Depends(get_db)):
    album = crud.get_album(db=db, album_id=album_id)
    photo = crud.get_photo(db=db, photo_id=cover_photo_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    elif not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return crud.update_album_cover(db=db, db_album=album, cover_photo_id=photo.id)


@router.get("/{album_id}/photos", response_model=list[Photo], status_code=200)
def read_album_photos(album_id: int, db: Session = Depends(get_db)):
    photos = crud.get_album_photos(db=db, album_id=album_id)
    return photos


@router.post("/{album_id}/upload", status_code=202)
def upload_album_photos(album_id: int, files: list[UploadFile], background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    album = crud.get_album(db=db, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    for file in files:
        file_path = save_photo_upload(file)
        background_tasks.add_task(process_photo_upload, db, album_id, file.filename, file_path)
    return {"received": [file.filename for file in files]}
