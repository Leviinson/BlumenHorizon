from django.db.models import Avg, Count, Prefetch
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from cart.cart import ProductCart
from core.services.mixins import CanonicalsContextMixin, CommonContextMixin
from core.services.mixins.canonicals import CanonicalLinksMixin

from ..filters import ProductFilter
from ..forms import ProductReviewForm
from ..models import Product, ProductImage, ProductReview, ProductsListPageModel
from ..services.mixins.views.details_mixin import DetailViewMixin
from ..services.mixins.views.list_mixin import ListViewMixin, ProductListViewMixin
from ..services.mixins.views.reviews import CreateItemReviewViewMixin


class ProductView(
    DetailViewMixin,
    CommonContextMixin,
    CanonicalsContextMixin,
    DetailView,
    CanonicalLinksMixin,
):
    model = Product
    queryset = (
        Product.objects.filter(is_active=True)
        .prefetch_related(
            "images",
            Prefetch(
                "reviews",
                queryset=ProductReview.objects.filter(is_published=True),
            ),
        )
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
            "images",
            "discount",
            "discount_expiration_datetime",
            "subcategory__slug",
            "subcategory__name",
            "subcategory__category__slug",
            "subcategory__category__name",
        )
        .annotate(avg_rating=Avg("reviews__rate"), rating_count=Count("reviews"))
    )
    context_object_name = "product"
    slug_url_kwarg = "product_slug"
    template_name = "catalog/base_detail.html"
    detail_url_name = "product-details"
    category_url_name = "products-category"
    subcategory_url_name = "products-subcategory"
    cart = ProductCart
    model = Product
    image_model = ProductImage
    item_details_viewname = "catalogue:product-review"


class ProductListView(
    ListViewMixin,
    ProductListViewMixin,
    CommonContextMixin,
    CanonicalsContextMixin,
    FilterView,
    TemplateResponseMixin,
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
            "discount_expiration_datetime",
            "subcategory__slug",
            "subcategory__category__slug",
        )
    )
    ordering = ("name",)
    context_object_name = "products"
    template_name = "catalog/base_list.html"
    filterset_class = ProductFilter
    image_model = ProductImage
    page_model = ProductsListPageModel
    form_class = ProductReviewForm
    http_method_names = [
        "get",
        "post",
    ]
    template_name = "catalog/review.html"
    success_url = reverse_lazy("mainpage:offers")
    context_object_name = "item"

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CreateProductReviewView(
    CreateItemReviewViewMixin,
    CommonContextMixin,
    FormMixin,
    DetailView,
):
    form_class = ProductReviewForm
    http_method_names = [
        "get",
        "post",
    ]
    queryset = (
        Product.objects.select_related("subcategory", "subcategory__category")
        .only(
            "name",
            "slug",
            "is_active",
            "subcategory__is_active",
            "subcategory__slug",
            "subcategory__category__is_active",
            "subcategory__category__slug",
        )
        .filter(
            is_active=True,
            subcategory__is_active=True,
            subcategory__category__is_active=True,
        )
    )
    template_name = "catalog/review.html"
    context_object_name = "item"
    slug_url_kwarg = "product_slug"
    image_model = ProductImage
    item_details_viewname = "catalogue:product-details"
