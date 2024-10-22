from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from core.services.mixins.views import CommonContextMixin

from ..models import Product
from ..services.views import ListViewMixin


class ProductView(
    CommonContextMixin,
    DetailView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Product
    queryset = Product.objects.filter(is_active=True).order_by("name")
    context_object_name = "product"
    slug_url_kwarg = "product_slug"
    template_name = "products/products/product_detail.html"


class ProductListView(
    ListViewMixin,
    CommonContextMixin,
    ListView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Product
    queryset = Product.objects.filter(is_active=True).order_by("name")
    context_object_name = "products"
    template_name = "products/products/product_list.html"
