import logging
from datetime import datetime
from exif import Image as ExifImage
from fastapi import UploadFile
from json import dumps
from os import makedirs, path, remove
from PIL import Image
from plum.exceptions import UnpackError
from shutil import copyfileobj
from sqlmodel import Session
from uuid import uuid4

from pixelperfect.core.settings import settings
from pixelperfect.db import crud
from pixelperfect.db.models import Photo

logger = logging.getLogger(__name__)
IMAGE_DIRECTORY = path.join(settings.BASE_DIRECTORY, "images")
IMAGE_THUMBNAIL_DIRECTORY = path.join(IMAGE_DIRECTORY, "thumbnails")


def get_exif_data(file_name: str) -> dict:
    try:
        image = ExifImage(file_name)
        return {tag: str(image.get(tag)) for tag in image.list_all()} if image.has_exif else {}
    except (UnpackError, ValueError):
        logger.warning(f'Unable to get exif data from: {file_name}')
        return {}


def save_photo_upload(upload_file: UploadFile):
    makedirs(IMAGE_DIRECTORY, exist_ok=True)
    target_file_name = str(uuid4()) + path.splitext(upload_file.filename)[1]
    with open(path.join(IMAGE_DIRECTORY, target_file_name), "wb+") as f:
        copyfileobj(upload_file.file, f)
        return f.name


def save_photo_resized(image: Image, file_name: str, size: int):
    image_resized_directory = path.join(IMAGE_DIRECTORY, str(size))
    makedirs(image_resized_directory, exist_ok=True)
    image.thumbnail((size, size))
    image.save(path.join(image_resized_directory, file_name), exif=image.getexif(), quality=95)


def save_photo_thumbnail(image: Image, file_name: str, size: int = 600):
    def crop_center(image: Image, crop_width: int, crop_height: int):
        img_width, img_height = image.size
        return image.crop(((img_width - crop_width) // 2,
                           (img_height - crop_height) // 2,
                           (img_width + crop_width) // 2,
                           (img_height + crop_height) // 2))

    def crop_max_square(image: Image):
        return crop_center(image, min(image.size), min(image.size))

    image_thumbnail = crop_max_square(image).resize((size, size), Image.LANCZOS)
    makedirs(IMAGE_THUMBNAIL_DIRECTORY, exist_ok=True)
    image_thumbnail.save(path.join(IMAGE_THUMBNAIL_DIRECTORY, file_name), exif=image.getexif(), quality=95)


def process_photo_upload(db: Session, album_id: int, name: str, file_name: str):
    image = Image.open(file_name)
    image_exif_data = get_exif_data(file_name)
    for size in settings.IMAGE_RESIZE_SIZES:
        save_photo_resized(image=image.copy(), file_name=path.basename(file_name), size=size)
    save_photo_thumbnail(image=image.copy(), file_name=path.basename(file_name))
    photo = Photo(album_id=album_id,
                  name=name,
                  date_taken=datetime.strptime(image_exif_data['datetime_original'], '%Y:%m:%d %H:%M:%S')
                  if 'datetime' in image_exif_data else datetime.now(),
                  file_name=path.basename(file_name),
                  format=image.format,
                  mode=image.mode,
                  width=image.width,
                  height=image.height,
                  exif_data=dumps(image_exif_data))
    crud.create_photo(db, photo)


def remove_photo_upload(file_name: str):
    def remove_photo_file(file_path: str):
        if path.exists(file_path):
            remove(file_path)
    remove_photo_file(path.join(IMAGE_DIRECTORY, file_name))
    remove_photo_file(path.join(IMAGE_THUMBNAIL_DIRECTORY, file_name))
    for size in settings.IMAGE_RESIZE_SIZES:
        remove_photo_file(path.join(path.join(IMAGE_DIRECTORY, str(size)), file_name))


def get_photo_image_path(file_name: str, size: str):
    file_path = path.join(IMAGE_DIRECTORY, file_name)
    if size and size == 'thumbnail':
        thumbnail_file_path = path.join(IMAGE_THUMBNAIL_DIRECTORY, file_name)
        if not path.exists(thumbnail_file_path):
            save_photo_thumbnail(image=Image.open(file_path), file_name=file_name)
        return thumbnail_file_path
    elif size:
        available_resizes = [s for s in settings.IMAGE_RESIZE_SIZES if s >= int(size)]
        if available_resizes:
            optimal_size = min(available_resizes)
            resized_file_path = path.join(path.join(IMAGE_DIRECTORY, str(optimal_size), file_name))
            if not path.exists(resized_file_path):
                save_photo_resized(image=Image.open(file_path), file_name=file_name, size=optimal_size)
            return resized_file_path
        else:
            return file_path
    else:
        return file_path
