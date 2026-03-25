from io import BytesIO
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from PIL import Image, UnidentifiedImageError


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")


def read_image_dimensions(file_obj) -> tuple[int, int]:
    try:
        file_obj.seek(0)
        with Image.open(file_obj) as image:
            width, height = image.size
    except (UnidentifiedImageError, OSError) as exc:
        raise ValidationError({"file": _("Uploaded file is not a valid image.")}) from exc
    finally:
        file_obj.seek(0)

    return width, height


def resize_image_for_limits(file_obj, filename: str, max_width: int, max_height: int):
    file_obj.seek(0)
    with Image.open(file_obj) as image:
        if image.width <= max_width and image.height <= max_height:
            width, height = image.size
            file_obj.seek(0)
            return None, None, width, height

        image_format = image.format or "PNG"
        image.thumbnail((max_width, max_height))
        width, height = image.size

        buffer = BytesIO()
        image.save(buffer, format=image_format)
        buffer.seek(0)

        normalized_extension = "jpg" if image_format.upper() == "JPEG" else image_format.lower()
        new_name = f"{Path(filename).stem}.{normalized_extension}"

    return new_name, ContentFile(buffer.read()), width, height


