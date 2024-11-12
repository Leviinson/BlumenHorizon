from django.contrib.auth.decorators import user_passes_test
from django.urls import include, path

from .views import image_upload


def superuser_required(function):
    return user_passes_test(lambda user: user.is_superuser)(function)


app_name = "tiny-mce"

urlpatterns = [
    path("tinymce/", superuser_required(include("tinymce.urls"))),
    path(
        "tinymce-image-upload/", superuser_required(image_upload), name="image_upload"
    ),
]
