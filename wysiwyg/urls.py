from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path

from .views import image_upload

app_name = "tiny-mce"

urlpatterns = [
    path("tinymce/", staff_member_required(include("tinymce.urls"))),
    path(
        "tinymce-image-upload/",
        staff_member_required(image_upload),
        name="image_upload",
    ),
]
