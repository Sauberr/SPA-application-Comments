from django.db import models
from django.utils.translation import gettext_lazy as _

from comments.services import (
    get_file_extension,
    read_image_dimensions,
    resize_image_for_limits,
)
from comments.validators import (
    validate_attachment_kind,
    validate_image_extension,
    validate_text_attachment,
)
from core.models import TimeStampedModel


class Attachment(TimeStampedModel):
    """Model for attachments related to comments."""

    MAX_TEXT_SIZE_BYTES = 100 * 1024
    MAX_IMAGE_WIDTH = 320
    MAX_IMAGE_HEIGHT = 240
    IMAGE_EXTENSIONS = {"jpg", "jpeg", "gif", "png"}

    KIND_IMAGE = "image"
    KIND_TEXT = "txt"
    KIND_CHOICES = [
        (KIND_IMAGE, "Image"),
        (KIND_TEXT, "Text"),
    ]
    ALLOWED_KINDS = {KIND_IMAGE, KIND_TEXT}

    comment = models.ForeignKey(
        "comments.Comment",
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("Comment"),
        help_text=_("The comment this attachment is associated with.")
    )
    file = models.FileField(
        upload_to='attachments/',
        verbose_name=_("File"),
        help_text=_("The file attached to the comment.")
    )
    kind = models.CharField(
        choices=KIND_CHOICES,
        max_length=20,
        verbose_name=_("Kind"),
        help_text=_("The type of the attachment (e.g., image, text).")
    )
    size_bytes = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Size (Bytes)"),
        help_text=_("The size of the attachment in bytes."),
    )
    image_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Image Width"),
        help_text=_("The width of the image in pixels (if applicable).")
    )
    image_height = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Image Height"),
        help_text=_("The height of the image in pixels (if applicable).")
    )

    def _set_file_size(self):
        self.size_bytes = self.file.size

    def _apply_text_metadata(self):
        self._set_file_size()
        self.image_width = None
        self.image_height = None

    def _apply_image_metadata(self):
        self.image_width, self.image_height = read_image_dimensions(self.file)
        self._set_file_size()

    def clean(self):
        super().clean()

        if not self.file:
            return

        extension = get_file_extension(self.file.name)
        validate_attachment_kind(self.kind, self.ALLOWED_KINDS)

        if self.kind == self.KIND_TEXT:
            validate_text_attachment(self.file, extension, self.MAX_TEXT_SIZE_BYTES)
            self._apply_text_metadata()
            return

        validate_image_extension(extension, self.IMAGE_EXTENSIONS)
        self._apply_image_metadata()

    def _resize_image_if_needed(self):
        if self.kind != self.KIND_IMAGE or not self.file:
            return

        new_name, content, width, height = resize_image_for_limits(
            self.file,
            self.file.name,
            self.MAX_IMAGE_WIDTH,
            self.MAX_IMAGE_HEIGHT,
        )

        if new_name and content:
            self.file.save(new_name, content, save=False)

        self.image_width = width
        self.image_height = height
        self._set_file_size()

    def save(self, *args, **kwargs):
        self.full_clean()
        self._resize_image_if_needed()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Attachment for Comment ID {self.comment_id} ({self.kind})"

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
        ordering = ['-created_at']
