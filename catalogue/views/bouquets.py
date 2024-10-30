from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django_filters.views import FilterView

from core.services.mixins.views import CommonContextMixin

from ..filters import BouquetFilter
from ..models import Bouquet, BouquetImage, Color, Flower
from ..services.views import DetailViewMixin, ListViewMixin


class BouquetView(
    DetailViewMixin,
    CommonContextMixin,
    DetailView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Bouquet
    queryset = (
        Bouquet.objects.filter(is_active=True)
        .prefetch_related("images", "colors", "flowers")
        .select_related(
            "subcategory",
            "subcategory__category",
        )
        .only(
            "name",
            "slug",
            "price",
            "amount_of_flowers",
            "description",
            "specs",
            "images",
            "discount",
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


class BouquetListView(
    ListViewMixin,
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
        "subcategory__slug",
        "subcategory__category__slug",
        "colors__name",
        "colors__hex_code",
        "flowers__name",
    )
    context_object_name = "products"
    template_name = "products/bouquets/bouquet_list.html"
    filterset_class = BouquetFilter
    extra_context = {"title": _("Каталог букетов")}
    image_model = BouquetImage
    image_model_related_name = "bouquet"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["colors"] = Color.objects.only("name", "hex_code").all()
        context["flowers"] = Flower.objects.only("name").all()
        return context
