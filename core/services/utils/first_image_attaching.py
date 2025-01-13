from django.conf import settings
from django.db.models import Case, CharField, Exists, OuterRef, Subquery, Value, When
from django.db.models.functions import Coalesce, Concat
from django.db.models.query import QuerySet
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

from catalogue.models import Bouquet, BouquetImage, Product, ProductImage


def annotate_first_image_and_alt(
    queryset: QuerySet[Bouquet | Product],
    image_model: ProductImage | BouquetImage,
    language: str,
) -> QuerySet[Bouquet | Product]:
    """
    Добавляет первое изображение (URL и alt текст) к каждому элементу в queryset.

    Этот метод использует подзапрос для получения первого изображения каждого объекта
    и добавляет к каждому элементу в queryset локализованный URL изображения и alt текст. 
    Если изображение отсутствует, то используется дефолтное изображение и текст.

    Параметры:
    - queryset: Отфильтрованный queryset, который будет аннотирован.
    - image_model: Модель изображений, используемая для получения изображений.
    - language: Код текущего языка для alt текста изображения.

    Возвращает:
    Обновлённый queryset с добавленными URL изображения и alt текстом.
    """
    first_image_subquery = image_model.objects.filter(item=OuterRef("pk")).order_by(
        "id"
    )[:1]
    first_image_uri_subquery = Subquery(first_image_subquery.values("image")[:1])
    return queryset.annotate(
        first_image_url=Case(
            When(
                Exists(
                    first_image_uri_subquery,
                ),
                then=Concat(
                    Value(settings.MEDIA_URL),
                    first_image_uri_subquery,
                ),
            ),
            default=Value(static("defaults/no-image.webp")),
            output_field=CharField(),
        ),
        first_image_alt=Coalesce(
            Subquery(first_image_subquery.values(f"image_alt_{language}")[:1]),
            Value(_("Изображение продукта временно недоступно.")),
            output_field=CharField(),
        ),
    )
