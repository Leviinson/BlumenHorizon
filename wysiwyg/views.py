import os

from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def image_upload(request):
    if request.method == "POST":
        image = request.FILES.get("file")
        if image:
            path = default_storage.save(os.path.join("wysiwyg", image.name), image)
            return JsonResponse({"location": default_storage.url(path)})
    return JsonResponse({"error": "Image upload failed"}, status=400)
