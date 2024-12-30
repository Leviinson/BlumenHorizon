"""
Обрабатывает загрузку изображений через TinyMCE.

Эта функция принимает POST-запрос с изображением, сохраняет его в хранилище по пути "wysiwyg/{image_name}"
и возвращает URL для доступа к изображению. Если изображение не прикреплено или произошла ошибка, 
функция возвращает ошибку с кодом состояния 400.

Возвращаемое значение:
    JsonResponse: Ответ с URL изображения или сообщение об ошибке.
"""

import os

from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def image_upload(request):
    """
    Обрабатывает POST-запрос для загрузки изображения через редактор TinyMCE.

    Принимает файл изображения через параметр "file", сохраняет его в папке "wysiwyg" 
    в хранилище файлов Django, и возвращает URL для доступа к изображению. Если загрузка
    не удалась или файл не был прикреплен, возвращает ошибку с сообщением и статусом 400.

    Аргументы:
        request (HttpRequest): Входящий HTTP-запрос.

    Возвращаемое значение:
        JsonResponse: Ответ с URL загруженного изображения в случае успеха, 
                      или сообщение об ошибке с кодом состояния 400.
    """
    if request.method == "POST":
        image = request.FILES.get("file")
        if image:
            path = default_storage.save(os.path.join("wysiwyg", image.name), image)
            return JsonResponse({"location": default_storage.url(path)})
    return JsonResponse({"error": "Image upload failed"}, status=400)