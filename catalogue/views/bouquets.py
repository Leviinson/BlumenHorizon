from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_filters.views import FilterView


from core.services.mixins.views import CommonContextMixin

from ..models import Bouquet
from ..services.views import ListViewMixin


class BouquetView(
    CommonContextMixin,
    DetailView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Bouquet
    queryset = Bouquet.objects.filter(is_active=True).order_by("name")
    context_object_name = "product"
    slug_url_kwarg = "bouquet_slug"
    template_name = "products/bouquets/bouquet_detail.html"

    def get_context_data(self, *args, **kwargs):
        kwargs["title"] = self.object.name
        return super().get_context_data(*args, **kwargs)
    

class BouquetListView(
    ListViewMixin,
    CommonContextMixin,
    ListView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Bouquet
    queryset = Bouquet.objects.filter(is_active=True).order_by("name")
    context_object_name = "products"
    template_name = "products/bouquets/bouquet_list.html"
