from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from mimetypes import guess_type
from smart_open import smart_open
from sqlmodel import Session
from typing import Union

from pixelperfect.db import crud
from pixelperfect.db.database import get_db
from pixelperfect.db.models import Photo
from pixelperfect.utils import get_photo_image_path, remove_photo_upload

router = APIRouter()


@router.get("/{photo_id}", response_model=Photo, status_code=200)
def read_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = crud.get_photo(db=db, photo_id=photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


@router.get("/{photo_id}/image", response_class=Response, status_code=200)
def read_photo_image(photo_id: int, size: Union[str, None] = None, db: Session = Depends(get_db)):
    photo = crud.get_photo(db=db, photo_id=photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    photo_path = get_photo_image_path(file_name=str(photo.file_name), size=size)
    return Response(smart_open(photo_path, mode='rb').read(), media_type=guess_type(photo_path)[0])


@router.delete("/{photo_id}", status_code=204)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = crud.get_photo(db=db, photo_id=photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    remove_photo_upload(photo.file_name)
    crud.remove_photo(db=db, photo=photo)
