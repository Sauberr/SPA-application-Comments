from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def username_validator() -> RegexValidator:
    """Validator for usernames to ensure they are alphanumeric and between 3 and 255 characters."""
    return RegexValidator(
        regex=r'^[a-zA-Z0-9]{3,255}$',
        message='Username must be alphanumeric and can include underscores.',
        code='invalid_username'
    )


def validate_attachment_kind(kind: str, allowed_kinds: set[str]):
    if kind not in allowed_kinds:
        raise ValidationError({"kind": _("Unsupported attachment type.")})


def validate_text_attachment(file_obj, extension: str, max_size_bytes: int):
    if extension != "txt":
        raise ValidationError({"file": _("Text attachment must have .txt extension.")})
    if file_obj.size > max_size_bytes:
        raise ValidationError({"file": _("Text file size must be <= 100 KB.")})


def validate_image_extension(extension: str, allowed_extensions: set[str]):
    if extension not in allowed_extensions:
        raise ValidationError({"file": _("Image must be JPG, GIF, or PNG.")})
