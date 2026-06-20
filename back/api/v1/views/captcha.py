from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.services import generate_captcha


class CaptchaView(APIView):
    """
    GET /api/v1/captcha/

    Returns a fresh captcha challenge.
    Response:
        {
            "key":   "<uuid>",          # send this back with your comment POST
            "image": "data:image/png;base64,..."  # render this as <img src=...>
        }

    The key is valid for 5 minutes and is one-time use — a new one is required
    after every comment submission (pass or fail).
    """

    def get(self, request: Request) -> Response:
        key, image = generate_captcha()
        return Response({"key": key, "image": image})
