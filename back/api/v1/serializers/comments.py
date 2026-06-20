import bleach
from rest_framework import serializers

from comments.models import Attachment, Comment
from comments.services import get_file_extension, verify_captcha

# Tags and attributes the user is allowed to use in comment text.
# Everything else is stripped by bleach to prevent XSS.
ALLOWED_TAGS = ["a", "code", "i", "strong"]
ALLOWED_ATTRIBUTES = {"a": ["href", "title"]}


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["id", "file", "kind", "size_bytes", "image_width", "image_height"]
        read_only_fields = fields


class CommentSerializer(serializers.ModelSerializer):
    """Read serializer — used for listing and retrieving comments.
    Recursively nests children so the full thread is returned in one response."""

    attachments = AttachmentSerializer(many=True, read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "reply_to",
            "username",
            "email",
            "homepage",
            "content",
            "created_at",
            "attachments",
            "children",
        ]

    def get_children(self, obj):
        qs = obj.children.prefetch_related("attachments", "children").all()
        return CommentSerializer(qs, many=True, context=self.context).data


class CommentCreateSerializer(serializers.ModelSerializer):
    """Write serializer — used when a user submits a new comment or reply.
    Sanitizes HTML in `content`, validates CAPTCHA, and handles optional file attachment.
    """

    captcha_key = serializers.CharField(write_only=True)
    captcha_value = serializers.CharField(write_only=True, max_length=20)
    attachment = serializers.FileField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = Comment
        fields = [
            "reply_to",
            "username",
            "email",
            "homepage",
            "content",
            "captcha_key",
            "captcha_value",
            "attachment",
        ]

    def validate_content(self, value: str) -> str:
        # bleach.clean strips every tag not in ALLOWED_TAGS.
        # strip=True removes the tag entirely (e.g. <script> → gone).
        # strip=False would escape it to &lt;script&gt; instead.
        cleaned = bleach.clean(
            value,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
        )
        if not cleaned.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return cleaned

    def validate(self, data):
        key = data.pop("captcha_key")
        value = data.pop("captcha_value")
        if not verify_captcha(key, value):
            raise serializers.ValidationError(
                {
                    "captcha_value": "Invalid or expired CAPTCHA. Please refresh and try again."
                }
            )
        return data

    def validate_attachment(self, file):
        ext = get_file_extension(file.name)
        allowed = Attachment.IMAGE_EXTENSIONS | {"txt"}
        if ext not in allowed:
            raise serializers.ValidationError(
                f"Unsupported file type '.{ext}'. Allowed: jpg, gif, png, txt."
            )
        return file

    def create(self, validated_data):
        attachment_file = validated_data.pop("attachment", None)
        comment = Comment.objects.create(**validated_data)

        if attachment_file:
            ext = get_file_extension(attachment_file.name)
            kind = (
                Attachment.KIND_IMAGE
                if ext in Attachment.IMAGE_EXTENSIONS
                else Attachment.KIND_TEXT
            )
            Attachment.objects.create(comment=comment, file=attachment_file, kind=kind)

        return comment
