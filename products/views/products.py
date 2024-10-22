from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django_filters import BooleanFilter, FilterSet
from django_filters.views import FilterView
from django import forms

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

    def get_context_data(self, *args, **kwargs):
        kwargs["title"] = self.object.name
        return super().get_context_data(*args, **kwargs)


class ProductFilter(FilterSet):
    with_discount = BooleanFilter(
        label="Со скидкой?",
        field_name="discount",
        method="filter_with_discount",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-dark'})
    )
    class Meta:
        model = Product
        fields = {
            "price": ["lt", "gt"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields["price__lt"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "price__lt",
                "min": 0,
            }
        )
        self.form.fields["price__gt"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "price__gt",
                "min": 0,
            }
        )

    def filter_with_discount(self, queryset, name, value):
        if value:
            return queryset.filter(discount__isnull=False).exclude(discount=0)
        return queryset


class ProductListView(
    ListViewMixin,
    CommonContextMixin,
    FilterView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Product
    queryset = Product.objects.filter(is_active=True).order_by("name")
    context_object_name = "products"
    template_name = "products/products/product_list.html"
    filterset_class = ProductFilter
