from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django_filters.views import FilterView

from core.services.mixins.views import CommonContextMixin

from ..filters import ProductFilter
from ..models import Product, ProductImage
from ..services.views import DetailViewMixin, ListViewMixin


class ProductView(
    DetailViewMixin,
    CommonContextMixin,
    DetailView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Product
    queryset = (
        Product.objects.filter(is_active=True)
        .prefetch_related("images")
        .select_related(
            "subcategory",
            "subcategory__category",
        )
        .only(
            "name",
            "price",
            "description",
            "specs",
            "images",
            "discount",
            "subcategory__slug",
            "subcategory__name",
            "subcategory__category__slug",
            "subcategory__category__name",
        )
    )
    context_object_name = "product"
    slug_url_kwarg = "product_slug"
    template_name = "products/base_detail.html"
    detail_url_name = "product-details"
    category_url_name = "products-category"
    subcategory_url_name = "products-subcategory"


class ProductListView(
    ListViewMixin,
    CommonContextMixin,
    FilterView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Product
    queryset = (
        Product.objects.filter(is_active=True)
        .select_related(
            "subcategory__category",
        )
        .only(
            "slug",
            "name",
            "price",
            "images",
            "discount",
            "subcategory__slug",
            "subcategory__category__slug",
        )
    )
    ordering = ("name",)
    context_object_name = "products"
    template_name = "products/base_list.html"
    filterset_class = ProductFilter
    extra_context = {"title": _("Каталог продуктов")}
    image_model = ProductImage
    image_model_related_name = "product"
