from django import forms
from django.db.models import Max, Min
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django_filters import BooleanFilter, FilterSet
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _
from core.services.mixins.views import CommonContextMixin

from ..models import Product, ProductImage
from ..services.views import ListViewMixin
from django.db.models import OuterRef, Subquery


class ProductView(
    CommonContextMixin,
    DetailView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Product
    queryset = (
        Product.objects.filter(is_active=True)
        .order_by("name")
        .prefetch_related("images")
        .only("name", "price", "description", "specs", "images", "discount")
    )
    context_object_name = "product"
    slug_url_kwarg = "product_slug"
    template_name = "products/products/product_detail.html"

    def get_context_data(self, *args, **kwargs):
        kwargs["title"] = self.object.name
        kwargs["images_url"] = (image.image.url for image in self.object.images.all())
        return super().get_context_data(*args, **kwargs)


class ProductFilter(FilterSet):
    with_discount = BooleanFilter(
        label="Со скидкой?",
        field_name="discount",
        method="filter_with_discount",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input checkbox-dark"}),
    )

    class Meta:
        model = Product
        fields = {
            "price": ["gte", "lte"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        price_limits = Product.objects.aggregate(
            min_price=Min("price"), max_price=Max("price")
        )
        self.form.fields["price__gte"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "price__gte",
                "min": 0,
                "max": (
                    price_limits["max_price"]
                    if price_limits["max_price"] is not None
                    else 0
                ),
            }
        )
        self.form.fields["price__lte"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "price__lte",
                "min": 0,
                "max": (
                    price_limits["max_price"]
                    if price_limits["max_price"] is not None
                    else 0
                ),
            }
        )

    def filter_with_discount(self, queryset, name, value):
        if value:
            queryset = queryset.filter(discount__gt=0)
            return queryset
        return queryset


class ProductListView(
    ListViewMixin,
    CommonContextMixin,
    FilterView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Product
    context_object_name = "products"
    template_name = "products/products/product_list.html"
    filterset_class = ProductFilter
    ordering = ("price",)
    extra_context = {"title": _("Каталог букетов")}

    def get_queryset(self):
        first_image_subquery = ProductImage.objects.filter(
            product=OuterRef('pk')
        ).order_by('id')[:1]

        return (
            Product.objects.filter(is_active=True)
            .order_by("name")
            .annotate(first_image=Subquery(first_image_subquery.values('image')[:1]))
        )
