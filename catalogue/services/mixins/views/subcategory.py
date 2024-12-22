from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from catalogue.models import BouquetSubcategory, ProductSubcategory
from catalogue.services.mixins.views.list_mixin import ListViewMixin


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
        context["meta_tags"] = self.subcategory.meta_tags
        context["subcategory"] = self.subcategory
        return context


class BouquetSubcategoryListViewMixin(SubcategoryListViewMixin):

    def get_queryset(self):
        qs = super().get_queryset()
        self.subcategory = get_object_or_404(
            BouquetSubcategory.objects.select_related("category").only(
                "name",
                "meta_tags",
                "category__name",
                "category__slug",
            ),
            slug=self.kwargs["subcategory_slug"],
            category__slug=self.kwargs["category_slug"],
            is_active=True,
        )
        return qs.filter(
            subcategory=self.subcategory,
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_subcategory_list"] = True
        context["is_bouquet_subcategory"] = True
        return context


class ProductSubcategoryListViewMixin(SubcategoryListViewMixin):

    def get_queryset(self):
        qs = super().get_queryset()
        self.subcategory = get_object_or_404(
            ProductSubcategory.objects.select_related("category").only(
                "name",
                "meta_tags",
                "category__name",
                "category__slug",
            ),
            slug=self.kwargs["subcategory_slug"],
            category__slug=self.kwargs["category_slug"],
            is_active=True,
        )
        return qs.filter(
            subcategory=self.subcategory,
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_subcategory_list"] = True
        context["is_product_subcategory"] = True
        return context
