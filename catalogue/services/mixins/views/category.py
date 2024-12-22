from django.shortcuts import get_object_or_404

from catalogue.models import BouquetCategory, ProductCategory
from catalogue.services.mixins.views.list_mixin import ListViewMixin


class CategoryListViewMixin(ListViewMixin):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["breadcrumbs"] = (
            {
                "name": self.category.name,
                "url": None,
            },
        )
        context["meta_tags"] = self.category.meta_tags
        context["category"] = self.category
        return context


class BouquetCategoryListViewMixin(CategoryListViewMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        self.category = get_object_or_404(
            BouquetCategory.objects.only(
                "name",
                "meta_tags",
            ),
            slug=self.kwargs["category_slug"],
            is_active=True,
        )
        return qs.filter(
            subcategory__category=self.category,
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_category_list"] = True
        context["is_bouquet_category"] = True
        return context


class ProductCategoryListViewMixin(CategoryListViewMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        self.category = get_object_or_404(
            ProductCategory.objects.only(
                "name",
                "meta_tags",
            ),
            slug=self.kwargs["category_slug"],
            is_active=True,
        )
        return qs.filter(
            subcategory__category=self.category,
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_category_list"] = True
        context["is_product_category"] = True
        return context
