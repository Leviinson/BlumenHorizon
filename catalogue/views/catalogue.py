from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from ..models import (
    BouquetCategory,
    BouquetSubcategory,
    ProductCategory,
    ProductSubcategory,
)
from .bouquets import BouquetListView
from .products import ProductListView
from ..services.views import ListViewMixin


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


class ProductCategoryListViewMixin(CategoryListViewMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        self.category = get_object_or_404(
            ProductCategory.objects.only("name"), slug=self.kwargs["category_slug"]
        )
        return qs.filter(
            subcategory__category=self.category,
        )


class ProductSubcategoryListViewMixin(SubcategoryListViewMixin):

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


class BouquetCategoryListViewMixin(CategoryListViewMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        self.category = get_object_or_404(
            BouquetCategory, slug=self.kwargs["category_slug"]
        )
        return qs.filter(
            subcategory__category=self.category,
        )


class BouquetSubcategoryListViewMixin(SubcategoryListViewMixin):

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
