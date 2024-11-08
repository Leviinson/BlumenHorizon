from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from cart.cart import BouquetCart, ProductCart
from catalogue.forms import IndividualQuestionForm

from ..models import (
    BouquetCategory,
    BouquetSubcategory,
    ProductCategory,
    ProductSubcategory,
)
from ..services.views import ListViewMixin
from .bouquets import BouquetListView
from .products import ProductListView


class CategoryListViewMixin(ListViewMixin):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["breadcrumbs"] = (
            {
                "name": self.category.name,
                "url": None,
            },
        )
        context["title"] = self.category.name
        return context


class SubcategoryListViewMixin(ListViewMixin):
    category_url_name = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if not (self.category_url_name):
            raise ValueError(
                "Name of the category url in urls.py has to be specified",
            )
        context["breadcrumbs"] = (
            {
                "name": self.subcategory.category.name,
                "url": reverse_lazy(
                    f"catalogue:{self.category_url_name}",
                    kwargs={
                        "category_slug": self.subcategory.category.slug,
                    },
                ),
            },
            {"name": self.subcategory.name, "url": None},
        )
        context["title"] = self.subcategory.name
        return context


class ProductListViewMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["products_cart"] = ProductCart(
            session=self.request.session, session_key="products_cart"
        )
        return context


class BouquetListViewMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["bouquets_cart"] = BouquetCart(
            session=self.request.session, session_key="bouquets_cart"
        )
        return context


class ProductCategoryListViewMixin(ProductListViewMixin, CategoryListViewMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        self.category = get_object_or_404(
            ProductCategory.objects.only("name"), slug=self.kwargs["category_slug"]
        )
        return qs.filter(
            subcategory__category=self.category,
        )


class ProductSubcategoryListViewMixin(ProductListViewMixin, SubcategoryListViewMixin):

    def get_queryset(self):
        qs = super().get_queryset()
        self.subcategory = get_object_or_404(
            ProductSubcategory.objects.select_related("category").only(
                "name", "category__name", "category__slug"
            ),
            slug=self.kwargs["subcategory_slug"],
            category__slug=self.kwargs["category_slug"],
        )
        return qs.filter(
            subcategory=self.subcategory,
        )


class BouquetCategoryListViewMixin(BouquetListViewMixin, CategoryListViewMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        self.category = get_object_or_404(
            BouquetCategory, slug=self.kwargs["category_slug"]
        )
        return qs.filter(
            subcategory__category=self.category,
        )


class BouquetSubcategoryListViewMixin(BouquetListViewMixin, SubcategoryListViewMixin):

    def get_queryset(self):
        qs = super().get_queryset()
        self.subcategory = get_object_or_404(
            BouquetSubcategory.objects.select_related("category").only(
                "name", "category__name", "category__slug"
            ),
            slug=self.kwargs["subcategory_slug"],
            category__slug=self.kwargs["category_slug"],
        )
        return qs.filter(
            subcategory=self.subcategory,
        )


class CategoryProductsListView(ProductCategoryListViewMixin, ProductListView):
    pass


class SubcategoryProductsListView(ProductSubcategoryListViewMixin, ProductListView):
    category_url_name = "products-category"


class CategoryBouquetListView(BouquetCategoryListViewMixin, BouquetListView):
    pass


class SubcategoryBouquetListView(BouquetSubcategoryListViewMixin, BouquetListView):
    category_url_name = "bouquets-category"


class IndividualQuestionView(CreateView):
    form_class = IndividualQuestionForm
    http_method_names = ["post"]

    def form_valid(self, form: IndividualQuestionForm):
        form.save(commit=True, user=self.request.user)
        return JsonResponse(
            {
                "message": _("Мы скоро с Вами свяжемся, а пока выпейте чаю 😊"),
                "status": "success",
            },
            status=201,
        )

    def form_invalid(self, form):
        return JsonResponse(
            {
                "message": _("Вы неправильно заполнили форму:"),
                "errors": form.errors.as_json(),
                "status": 400,
            },
            status=400,
        )

    def http_method_not_allowed(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(
            {
                "message": _("Метод не разрешен. Используйте POST."),
                "status": 405,
            },
            status=405,
        )
