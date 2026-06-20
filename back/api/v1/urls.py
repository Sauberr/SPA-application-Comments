from django.urls import path

from api.v1.views.captcha import CaptchaView
from api.v1.views.comments import CommentDetailView, CommentListCreateView

urlpatterns = [
    path("captcha/", CaptchaView.as_view(), name="captcha"),
    path("comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
]
