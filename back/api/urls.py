from django.urls import include, path

urlpatterns = [
    path("v1/", include("api.v1.urls")),
    # When v2 is needed:
    # path("v2/", include("api.v2.urls")),
]