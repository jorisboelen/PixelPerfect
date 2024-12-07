import logging
from cloudpathlib import S3Path
from datetime import datetime
from exif import Image as ExifImage
from fastapi import UploadFile
from json import dumps
from os import makedirs, remove
from os.path import basename, join, splitext
from PIL import Image
from plum.exceptions import UnpackError
from shutil import copyfileobj
from smart_open import open as smart_open
from sqlmodel import Session
from typing import BinaryIO
from uuid import uuid4

from pixelperfect.core.settings import settings
from pixelperfect.db import crud
from pixelperfect.db.models import Photo

try:
    import boto3
except ImportError:
    boto3 = None

logger = logging.getLogger(__name__)


def smart_exists(file_path: str):
    try:
        with smart_open(file_path, mode='rb'):
            return True
    except (FileNotFoundError, OSError):
        return False


def smart_makedirs(directory_path: str, exist_ok: bool=True):
    if directory_path.startswith('s3://'):
        pass
    else:
        makedirs(directory_path, exist_ok=exist_ok)


def smart_remove(file_path: str):
    if smart_exists(file_path):
        if file_path.startswith('s3://'):
            s3_path = S3Path(file_path)
            boto3.resource('s3').Object(s3_path.bucket, s3_path.key).delete()
        else:
            remove(file_path)


def get_exif_data(file: BinaryIO) -> dict:
    try:
        image = ExifImage(file)
        return {tag: str(image.get(tag)) for tag in image.list_all()} if image.has_exif else {}
    except (UnpackError, ValueError):
        logger.warning(f'Unable to get exif data from: {file.name}')
        return {}


def save_photo_upload(upload_file: UploadFile):
    smart_makedirs(settings.IMAGE_DIRECTORY, exist_ok=True)
    target_file_path = join(settings.IMAGE_DIRECTORY, str(uuid4()) + splitext(upload_file.filename)[1])
    with smart_open(target_file_path, "wb") as f:
        copyfileobj(upload_file.file, f)
        return target_file_path


def save_photo_resized(image: Image, image_format: str, file_name: str, size: int):
    image_resized_directory = join(settings.IMAGE_DIRECTORY, str(size))
    smart_makedirs(image_resized_directory, exist_ok=True)
    image.thumbnail((size, size))
    with smart_open(join(image_resized_directory, file_name), "wb") as f:
        image.save(f, format=image_format, exif=image.getexif(), quality=95)


def save_photo_thumbnail(image: Image, image_format: str, file_name: str, size: int = 600):
    def crop_center(image: Image, crop_width: int, crop_height: int):
        img_width, img_height = image.size
        return image.crop(((img_width - crop_width) // 2,
                           (img_height - crop_height) // 2,
                           (img_width + crop_width) // 2,
                           (img_height + crop_height) // 2))

    def crop_max_square(image: Image):
        return crop_center(image, min(image.size), min(image.size))

    image_thumbnail = crop_max_square(image).resize((size, size), Image.LANCZOS)
    image_thumbnail_directory = join(settings.IMAGE_DIRECTORY, 'thumbnails')
    smart_makedirs(image_thumbnail_directory, exist_ok=True)
    with smart_open(join(image_thumbnail_directory, file_name), "wb") as f:
        image_thumbnail.save(f, format=image_format, exif=image.getexif(), quality=95)


def process_photo_upload(db: Session, album_id: int, name: str, file_path: str):
    with smart_open(file_path, mode='rb') as f:
        image_exif_data = get_exif_data(f)
        image = Image.open(f)
        for size in settings.IMAGE_RESIZE_SIZES:
            save_photo_resized(image=image.copy(), image_format=image.format, file_name=basename(file_path), size=size)
        save_photo_thumbnail(image=image.copy(), image_format=image.format, file_name=basename(file_path))
        photo = Photo(album_id=album_id,
                      name=name,
                      date_taken=datetime.strptime(image_exif_data['datetime_original'], '%Y:%m:%d %H:%M:%S')
                      if 'datetime' in image_exif_data else datetime.now(),
                      file_name=basename(file_path),
                      format=image.format,
                      mode=image.mode,
                      width=image.width,
                      height=image.height,
                      exif_data=dumps(image_exif_data))
        return crud.create_photo(db, photo)


def remove_photo_upload(file_name: str):
    smart_remove(join(settings.IMAGE_DIRECTORY, file_name))
    smart_remove(join(join(settings.IMAGE_DIRECTORY, 'thumbnails'), file_name))
    for size in settings.IMAGE_RESIZE_SIZES:
        smart_remove(join(join(settings.IMAGE_DIRECTORY, str(size)), file_name))


def get_photo_image_path(file_name: str, size: str):
    file_path = join(settings.IMAGE_DIRECTORY, file_name)
    if size and size == 'thumbnail':
        thumbnail_file_path = (join(join(settings.IMAGE_DIRECTORY, 'thumbnails'), file_name))
        if not smart_exists(thumbnail_file_path):
            with smart_open(file_path, mode='rb') as f:
                image = Image.open(f)
                save_photo_thumbnail(image=image, image_format=image.format, file_name=file_name)
        return thumbnail_file_path
    elif size:
        available_resizes = [s for s in settings.IMAGE_RESIZE_SIZES if s >= int(size)]
        if available_resizes:
            optimal_size = min(available_resizes)
            resized_file_path = join(join(settings.IMAGE_DIRECTORY, str(optimal_size), file_name))
            if not smart_exists(resized_file_path):
                with smart_open(file_path, mode='rb') as f:
                    image = Image.open(f)
                    save_photo_resized(image=image, image_format=image.format, file_name=file_name, size=optimal_size)
            return resized_file_path
        else:
            return file_path
    else:
        return file_path
