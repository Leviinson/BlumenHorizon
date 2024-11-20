from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import BouquetCart
from core.services.mixins.views import CommonContextMixin

from ..filters import BouquetFilter
from ..models import (
    Bouquet,
    BouquetImage,
    BouquetSize,
    BouquetsListPageModel,
    Color,
    Flower,
)
from ..services.views import BouquetListViewMixin, DetailViewMixin, ListViewMixin
from .serializers import BouquetSizeSerializer


class GetBouquetSizes(APIView):
    def get(self, request, category_slug, subcategory_slug, bouquet_slug):
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
    DetailView,
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
            "json_ld",
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
    template_name = "products/bouquets/bouquet_detail.html"
    detail_url_name = "bouquet-details"
    category_url_name = "bouquets-category"
    subcategory_url_name = "bouquets-subcategory"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["bouquets_cart"] = BouquetCart(
            session=self.request.session, session_key="bouquets_cart"
        )
        return context


class BouquetListView(
    ListViewMixin,
    BouquetListViewMixin,
    CommonContextMixin,
    FilterView,
    TemplateResponseMixin,
    ContextMixin,
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
    template_name = "products/bouquets/bouquet_list.html"
    filterset_class = BouquetFilter
    image_model = BouquetImage
    image_model_related_name = "bouquet"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["colors"] = Color.objects.only("name", "hex_code").all()
        context["flowers"] = Flower.objects.only("name").all()
        page_model = BouquetsListPageModel.objects.first()
        context["meta_tags"] = page_model.meta_tags
        context["json_ld"] = page_model.json_ld
        return context
