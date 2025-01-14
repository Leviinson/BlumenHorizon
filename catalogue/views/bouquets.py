from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import BouquetCart
from core.services.mixins import CommonContextMixin, CanonicalsContextMixin
from core.services.mixins.canonicals import CanonicalLinksMixin

from ..filters import BouquetFilter
from ..models import (
    Bouquet,
    BouquetImage,
    BouquetSize,
    BouquetsListPageModel,
    Color,
    Flower,
)
from ..services.mixins.views.details_mixin import DetailViewMixin
from ..services.mixins.views.list_mixin import BouquetListViewMixin, ListViewMixin
from .serializers import BouquetSizeSerializer


class GetBouquetSizesView(APIView):
    """
    API-вью для получения доступных размеров конкретного букета.

    Этот эндпоинт позволяет пользователям получить размеры букета,
    идентифицируемого с помощью slug категории, подкатегории и самого букета.
    Букет и связанные объекты должны быть активными для успешного получения данных.
    """

    def get(
        self,
        request: Request,
        category_slug: str,
        subcategory_slug: str,
        bouquet_slug: str,
    ):
        """
        Обрабатывает GET-запрос для получения размеров букета.

        Аргументы:
            request (Request): HTTP-запрос.
            category_slug (str): Slug категории букета.
            subcategory_slug (str): Slug подкатегории букета.
            bouquet_slug (str): Slug букета.

        Возвращает:
            Response: JSON-ответ с сериализованными размерами букета,
            если они найдены, или соответствующее сообщение об ошибке.

        Исключения:
            NotFound: Если не найден активный букет или доступные размеры букета,
            соответствующие переданным slug.
        """
        bouquet = get_object_or_404(
            Bouquet.objects.select_related("subcategory__category").only(
                "id",
                "subcategory__category__slug",
                "subcategory__slug",
                "slug",
            ),
            slug=bouquet_slug,
            is_active=True,
            subcategory__slug=subcategory_slug,
            subcategory__is_active=True,
            subcategory__category__slug=category_slug,
            subcategory__category__is_active=True,
        )

        bouquet_sizes = (
            BouquetSize.objects.filter(bouquet=bouquet)
            .only("id", "price", "discount", "diameter", "amount_of_flowers")
            .prefetch_related("images")
        )

        if not bouquet_sizes.exists():
            raise NotFound("No bouquet sizes found for this bouquet.", 200)

        serializer = BouquetSizeSerializer(
            bouquet_sizes, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class BouquetView(
    DetailViewMixin,
    CommonContextMixin,
    CanonicalsContextMixin,
    DetailView,
    CanonicalLinksMixin,
):
    model = Bouquet
    queryset = (
        Bouquet.objects.prefetch_related(
            "images",
            "colors",
            "flowers",
            "sizes",
        )
        .select_related(
            "subcategory",
            "subcategory__category",
        )
        .only(
            "name",
            "slug",
            "price",
            "amount_of_flowers",
            "diameter",
            "sku",
            "description",
            "specs",
            "meta_tags",
            "images",
            "discount",
            "discount_expiration_datetime",
            "subcategory__slug",
            "subcategory__name",
            "subcategory__category__slug",
            "subcategory__category__name",
            "colors__name",
            "colors__hex_code",
            "flowers__name",
        )
    )
    context_object_name = "product"
    slug_url_kwarg = "bouquet_slug"
    template_name = "catalog/bouquets/bouquet_detail.html"
    category_url_name = "bouquets-category"
    subcategory_url_name = "bouquets-subcategory"
    cart = BouquetCart
    model = Bouquet
    image_model = BouquetImage


class BouquetListView(
    ListViewMixin,
    BouquetListViewMixin,
    CommonContextMixin,
    CanonicalsContextMixin,
    FilterView,
    TemplateResponseMixin,
):
    model = Bouquet
    queryset = Bouquet.objects.select_related(
        "subcategory__category",
    ).only(
        "slug",
        "name",
        "price",
        "images",
        "discount",
        "discount_expiration_datetime",
        "subcategory__slug",
        "subcategory__category__slug",
        "colors__name",
        "colors__hex_code",
        "flowers__name",
    )
    context_object_name = "products"
    template_name = "catalog/bouquets/bouquet_list.html"
    filterset_class = BouquetFilter
    image_model = BouquetImage
    page_model = BouquetsListPageModel

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["colors"] = Color.objects.only("name", "hex_code").all()
        context["flowers"] = Flower.objects.only("name").all()
        return context
