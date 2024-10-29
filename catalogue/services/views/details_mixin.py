from typing import Any

from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class DetailViewMixin:
    category_url_name = None
    subcategory_url_name = None

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        if not (self.category_url_name and self.subcategory_url_name):
            raise ValueError(
                "Category url and subcategory url name from urls.py must be specified."
            )
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.object.name
        context["images_url"] = (image.image.url for image in self.object.images.all())
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
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj
