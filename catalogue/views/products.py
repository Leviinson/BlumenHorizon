from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django_filters.views import FilterView

from cart.cart import ProductCart
from core.services.mixins.views import CommonContextMixin

from ..filters import ProductFilter
from ..models import Product, ProductImage, ProductsListPageModel
from ..services.views import DetailViewMixin, ListViewMixin, ProductListViewMixin


class ProductView(
    DetailViewMixin,
    CommonContextMixin,
    DetailView,
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
            "sku",
            "slug",
            "price",
            "description",
            "specs",
            "meta_tags",
            "json_ld",
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["products_cart"] = ProductCart(
            session=self.request.session, session_key="products_cart"
        )
        return context


class ProductListView(
    ListViewMixin,
    ProductListViewMixin,
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
    image_model = ProductImage
    image_model_related_name = "product"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_model = ProductsListPageModel.objects.first()
        context["meta_tags"] = page_model.meta_tags
        context["json_ld"] = page_model.json_ld
        return context
