from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from catalogue.models import BouquetCategory, ProductCategory
from catalogue.services.mixins.views.list_mixin import ListViewMixin
from core.services.mixins.canonicals import CanonicalLinksMixin


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


class BouquetCategoryListViewMixin(CategoryListViewMixin, CanonicalLinksMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        self.category = get_object_or_404(
            BouquetCategory.objects.only(
                "name",
                "meta_tags",
                "slug",
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

    @property
    def relative_url(self):
        return reverse_lazy(
            "catalogue:bouquets-category",
            kwargs={"category_slug": self.category.slug},
        )


class ProductCategoryListViewMixin(CategoryListViewMixin, CanonicalLinksMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        self.category = get_object_or_404(
            ProductCategory.objects.only(
                "name",
                "meta_tags",
                "slug",
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

    @property
    def relative_url(self):
        return reverse_lazy(
            "catalogue:products-category",
            kwargs={"category_slug": self.category.slug},
        )
