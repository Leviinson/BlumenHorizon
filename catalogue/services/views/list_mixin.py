from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from cart.cart import BouquetCart, ProductCart
from catalogue.models import (
    BouquetCategory,
    BouquetSubcategory,
    ProductCategory,
    ProductSubcategory,
)


class ListViewMixin:
    allow_empty = True
    paginate_by = 8
    image_model = None
    image_model_related_name = None

    SORT_OPTIONS = [
        {"name": _("Цена по убыванию"), "value": "pd"},
        {"name": _("Цена по возрастанию"), "value": "pi"},
        {"name": _("По алфавиту"), "value": "alph"},
        {"name": _("Со скидкой"), "value": "disc"},
    ]

    def get_queryset(self):
        qs = super().get_queryset()

        sort_option = self.request.GET.get("sort", "pd")

        match sort_option:
            case "pd":
                qs = qs.order_by("-price")
            case "pi":
                qs = qs.order_by("price")
            case "alph":
                qs = qs.order_by("name")
            case "disc":
                qs = qs.order_by("-discount")

        first_image_subquery = self.image_model.objects.filter(
            **{
                self.image_model_related_name: OuterRef("pk"),
            }
        ).order_by("id")[:1]
        return qs.filter(
            is_active=True,
            subcategory__is_active=True,
            subcategory__category__is_active=True,
        ).annotate(
            first_image_uri=Subquery(first_image_subquery.values("image")[:1]),
            first_image_alt=Subquery(first_image_subquery.values("image_alt")[:1]),
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["sort_options"] = self.SORT_OPTIONS
        return context


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
        context["meta_tags"] = self.subcategory.meta_tags
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


class ProductCategoryListViewMixin(CategoryListViewMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        self.category = get_object_or_404(
            ProductCategory.objects.only("name", "meta_tags"),
            slug=self.kwargs["category_slug"],
        )
        return qs.filter(
            subcategory__category=self.category,
        )


class ProductSubcategoryListViewMixin(SubcategoryListViewMixin):

    def get_queryset(self):
        qs = super().get_queryset()
        self.subcategory = get_object_or_404(
            ProductSubcategory.objects.select_related("category").only(
                "name", "meta_tags", "category__name", "category__slug"
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
            BouquetCategory.objects.only("name", "meta_tags"),
            slug=self.kwargs["category_slug"],
        )
        return qs.filter(
            subcategory__category=self.category,
        )


class BouquetSubcategoryListViewMixin(SubcategoryListViewMixin):

    def get_queryset(self):
        qs = super().get_queryset()
        self.subcategory = get_object_or_404(
            BouquetSubcategory.objects.select_related("category").only(
                "name", "meta_tags", "category__name", "category__slug"
            ),
            slug=self.kwargs["subcategory_slug"],
            category__slug=self.kwargs["category_slug"],
        )
        return qs.filter(
            subcategory=self.subcategory,
        )
