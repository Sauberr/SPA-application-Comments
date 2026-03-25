from django.core.validators import MinLengthValidator
from django.db import models
from core.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from comments.validators import username_validator


class Comment(TimeStampedModel):
    """Model for comments"""

    reply_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name=_("Reply To"),
        help_text=_("Reference to the parent comment if this comment is a reply.")
    )
    username = models.CharField(
        max_length=255,
        db_index=True,
        validators=[username_validator()],
        verbose_name=_("Username"),
        help_text=_("Name of the user who made the comment.")
    )
    email = models.EmailField(
        max_length=255,
        db_index=True,
        verbose_name=_("Email"),
        help_text=_("Email address of the user who made the comment.")
    )
    homepage = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Homepage"),
        help_text=_("Optional homepage URL of the user.")
    )
    content = models.TextField(
        validators=[MinLengthValidator(1)],
        verbose_name=_("Content"),
        help_text=_("The content of the comment.")
    )

    def __str__(self):
        return f"Comment by {self.username} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']

