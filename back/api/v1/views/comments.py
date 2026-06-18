from django.db.models import Prefetch
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.v1.serializers.comments import CommentCreateSerializer, CommentSerializer
from comments.models import Attachment, Comment


class CommentPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 25


class CommentListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/comments/           — paginated list of top-level comments
    POST /api/v1/comments/           — create a new comment or reply

    Sorting via ?sort= query param:
      username | -username | email | -email | created_at | -created_at
    Default sort: -created_at (newest first, LIFO)
    """

    pagination_class = CommentPagination

    _ALLOWED_SORT_FIELDS = {
        "username", "-username",
        "email", "-email",
        "created_at", "-created_at",
    }
    _DEFAULT_SORT = "-created_at"

    def get_queryset(self):
        sort = self.request.query_params.get("sort", self._DEFAULT_SORT)
        if sort not in self._ALLOWED_SORT_FIELDS:
            sort = self._DEFAULT_SORT

        # Prefetch 2 levels of children with their attachments to avoid N+1 queries
        grandchildren_qs = Comment.objects.prefetch_related(
            Prefetch("attachments", queryset=Attachment.objects.all()),
        )
        children_qs = Comment.objects.prefetch_related(
            Prefetch("attachments", queryset=Attachment.objects.all()),
            Prefetch("children", queryset=grandchildren_qs),
        )

        return (
            Comment.objects
            .filter(reply_to__isnull=True)
            .prefetch_related(
                Prefetch("attachments", queryset=Attachment.objects.all()),
                Prefetch("children", queryset=children_qs),
            )
            .order_by(sort)
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentCreateSerializer
        return CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response(
            CommentSerializer(comment, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class CommentDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/comments/<id>/  — retrieve a single comment with all nested replies
    """

    serializer_class = CommentSerializer

    def get_queryset(self):
        grandchildren_qs = Comment.objects.prefetch_related(
            Prefetch("attachments", queryset=Attachment.objects.all()),
        )
        children_qs = Comment.objects.prefetch_related(
            Prefetch("attachments", queryset=Attachment.objects.all()),
            Prefetch("children", queryset=grandchildren_qs),
        )
        return Comment.objects.prefetch_related(
            Prefetch("attachments", queryset=Attachment.objects.all()),
            Prefetch("children", queryset=children_qs),
        )