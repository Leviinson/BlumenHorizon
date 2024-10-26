from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_filters.views import FilterView


from core.services.mixins.views import CommonContextMixin

from ..models import Product
from ..services.views import ListViewMixin
    

class CategoryProductsListView(
    ListViewMixin,
    CommonContextMixin,
    ListView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Product
    queryset = Product.objects.filter(is_active=True).order_by("name")
    context_object_name = "products"
    template_name = "products/bouquets/bouquet_list.html"

class SubcategoryProductsListView(
    ListViewMixin,
    CommonContextMixin,
    ListView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Product
    queryset = Product.objects.filter(is_active=True).order_by("name")
    context_object_name = "products"
    template_name = "products/bouquets/bouquet_list.html"
