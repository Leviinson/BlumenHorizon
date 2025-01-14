from django.db.models.manager import BaseManager

from catalogue.models import Bouquet, BouquetImage, Product, ProductImage
from core.services.utils.first_image_attaching import annotate_first_image_and_alt

from ..dataclasses.related_model import RelatedModel
from ..types import OrderedModelField


def get_recommended_items_with_first_image(
    model: Product | Bouquet,
    image_model: ProductImage | BouquetImage,
    related_models: list[RelatedModel],
    order_fields: list[OrderedModelField],
    limit: int = 12,
) -> BaseManager[Product] | BaseManager[Bouquet]:
    """
    Функция для получения рекомендованных продуктов или букетов с аннотированным первым изображением.

    Эта функция выполняет запрос к базе данных, извлекая рекомендованные продукты или букеты с
    первым изображением. Изображения аннотируются с помощью подзапроса, который выбирает первое
    изображение для каждого продукта или букета. Результаты сортируются по заданным полям.

    :param model: Модель, для которой выполняется запрос (например, Bouquet или Product).
    :param image_model: Модель изображения, которая будет использоваться для подзапроса
                        (например, BouquetImage или ProductImage).
    :param related_models: Список связанных моделей с аттрибутами для выборки.
                        Например, >>> {"subcategory": ["slug"], "subcategory__category": ["slug"]}.
    :param order_fields: Список полей, по которым будет выполняться сортировка результата.
    :param limit: Количество элементов, которые будут возвращены. По умолчанию 12.
    :return: Менеджер запросов (BaseManager) с аннотированными объектами.

    Функция возвращает менеджер запросов с объектами, которые включают аннотированные данные о первом
    изображении каждого продукта или букета. Эти объекты можно использовать для дальнейшего извлечения
    данных или их отображения в интерфейсе пользователя.
    """
    from django.utils.translation import get_language

    language = get_language()
    related_fields = __get_related_fields(related_models)

    queryset = model.objects.select_related(*[rm.model for rm in related_models]).only(
        "name",
        "price",
        "slug",
        "sku",
        "discount",
        "description",
        "discount_expiration_datetime",
        *related_fields,
    )
    queryset_with_atteched_first_images = annotate_first_image_and_alt(
        queryset, image_model, language
    )
    return queryset_with_atteched_first_images.order_by(*order_fields)[:limit]


def __get_related_fields(related_models: list[RelatedModel]) -> list[str]:
    result = []
    for related_model in related_models:
        for field in related_model.fields:
            result.append(f"{related_model.model}__{field}")
    return result
