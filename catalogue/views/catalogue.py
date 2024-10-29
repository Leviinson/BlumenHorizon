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


class ProductCategoryListViewMixin:
    def get_queryset(self):
        self.category = get_object_or_404(
            ProductCategory, slug=self.kwargs["category_slug"]
        )
        qs = super().get_queryset()
        return qs.filter(
            subcategory__category=self.category,
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["breadcrumbs"] = ({"name": self.category.name, "url": None},)
        return context


class ProductSubcategoryListViewMixin:
    category_url_name = None

    def get_queryset(self):
        self.subcategory = get_object_or_404(
            ProductSubcategory.objects.select_related("category"),
            slug=self.kwargs["subcategory_slug"],
            category__slug=self.kwargs["category_slug"]
        )
        qs = super().get_queryset()
        return qs.filter(
            subcategory=self.subcategory,
        )

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
        return context


class BouquetCategoryListViewMixin:
    def get_queryset(self):
        self.category = get_object_or_404(
            BouquetCategory, slug=self.kwargs["category_slug"]
        )
        qs = super().get_queryset()
        return qs.filter(
            subcategory__category=self.category,
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["breadcrumbs"] = ({"name": self.category.name, "url": None},)
        return context


class BouquetSubcategoryListViewMixin:
    category_url_name = None

    def get_queryset(self):
        self.subcategory = get_object_or_404(
            BouquetSubcategory.objects.select_related("category"),
            slug=self.kwargs["subcategory_slug"],
            category__slug=self.kwargs["category_slug"]
        )
        qs = super().get_queryset()
        return qs.filter(
            subcategory=self.subcategory,
        )

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
        return context


class CategoryProductsListView(ProductCategoryListViewMixin, ProductListView):
    pass


class SubcategoryProductsListView(ProductSubcategoryListViewMixin, ProductListView):
    category_url_name = "products-category"


class CategoryBouquetListView(BouquetCategoryListViewMixin, BouquetListView):
    pass


class SubcategoryBouquetListView(BouquetSubcategoryListViewMixin, BouquetListView):
    category_url_name = "bouquets-category"
