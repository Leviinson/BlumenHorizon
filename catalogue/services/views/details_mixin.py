from typing import Any, Literal

from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from cart.cart import BouquetCart, ProductCart
from catalogue.forms import IndividualQuestionForm
from catalogue.models import Bouquet, BouquetImage, Product, ProductImage
from core.services.dataclasses import RelatedModel
from core.services.utils import get_recommended_items_with_first_image


class DetailViewMixin:
    category_url_name: str
    subcategory_url_name: str
    cart: ProductCart | BouquetCart
    model: Product | Bouquet
    image_model: ProductImage | BouquetImage
    image_filter_field: Literal["product", "bouquet"]

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        if not (self.category_url_name and self.subcategory_url_name):
            raise ValueError(
                "Category url and subcategory url name from urls.py must be specified."
            )
        context = super().get_context_data(*args, **kwargs)
        context["meta_tags"] = self.object.meta_tags
        context["breadcrumbs"] = [
            {
                "name": self.object.subcategory.category.name,
                "url": reverse_lazy(
                    f"catalogue:{self.category_url_name}",
                    kwargs={
                        "category_slug": self.object.subcategory.category.slug,
                    },
                ),
            },
            {
                "name": self.object.subcategory.name,
                "url": reverse_lazy(
                    f"catalogue:{self.subcategory_url_name}",
                    kwargs={
                        "category_slug": self.object.subcategory.category.slug,
                        "subcategory_slug": self.object.subcategory.slug,
                    },
                ),
            },
            {"name": self.object.name, "url": None},
        ]
        context["individual_question_form"] = IndividualQuestionForm()
        context["cart"] = self.cart(
            session=self.request.session, session_key="products_cart"
        )
        related_models = [
            RelatedModel(model="subcategory", attributes=["slug", "name"]),
            RelatedModel(model="subcategory__category", attributes=["slug"]),
        ]
        context["recommended_products"] = get_recommended_items_with_first_image(
            model=self.model,
            image_model=self.image_model,
            related_models=related_models,
            image_filter_field=self.image_filter_field,
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
        )
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            is_active=True,
            subcategory__is_active=True,
            subcategory__category__is_active=True,
        )

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = queryset.get(
                subcategory__category__slug=self.kwargs["category_slug"],
                subcategory__slug=self.kwargs["subcategory_slug"],
                slug=self.kwargs[self.slug_url_kwarg],
            )
        except queryset.model.DoesNotExist:
            raise Http404(
                _("Не найдено ни одного %(verbose_name)s совпадающего по запросу")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj
