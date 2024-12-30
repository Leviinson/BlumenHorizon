from django.db.models import OuterRef, Subquery
from django.db.models.manager import BaseManager

from catalogue.models import Bouquet, BouquetImage, Product, ProductImage

from ..dataclasses.related_model import RelatedModel


def get_recommended_items_with_first_image(
    model: Product | Bouquet,
    image_model: ProductImage | BouquetImage,
    related_models: list[RelatedModel],
    order_fields: list[str],
    limit: int = 12,
) -> BaseManager[Product] | BaseManager[Bouquet]:
    """
    A function to retrieve recommended products or bouquets with an annotated first image.

    :param model: The model for which the query is executed (e.g., Bouquet or Product).
    :param image_model: The image model that will be used for the subquery (e.g., BouquetImage or ProductImage).
    :param related_models: A dictionary where the key is the related model and the value is a list of attributes for that model.
                        For example, {"subcategory": ["slug"], "subcategory__category": ["slug"]}.
    :param order_fields: A list of fields to order the result by.
    :param limit: Amount of items, that will be returned.
    :return: A queryset with annotated objects.
    """
    from django.utils.translation import get_language

    language = get_language()

    first_image_subquery = (
        image_model.objects.filter(
            **{image_model.image_related_model_field: OuterRef("pk")}
        )
        .order_by("id")[:1]
        .values("image")
    )
    select_related_fields = []
    for related_model in related_models:
        for attr in related_model.attributes:
            select_related_fields.append(f"{related_model.model}__{attr}")

    queryset = (
        model.objects.select_related(*[rm.model for rm in related_models])
        .only(
            "name",
            "price",
            "slug",
            "sku",
            "discount",
            "description",
            "discount_expiration_datetime",
            *select_related_fields,
        )
        .annotate(
            first_image_uri=Subquery(
                first_image_subquery,
            ),
            first_image_alt=Subquery(
                first_image_subquery.values(f"image_alt_{language}")[:1],
            ),
        )
        .order_by(*order_fields)[:limit]
    )
    return queryset
